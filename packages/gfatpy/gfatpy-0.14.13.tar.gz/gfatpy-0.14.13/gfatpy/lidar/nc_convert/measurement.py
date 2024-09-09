from ast import parse
from codecs import ignore_errors
import re
import shutil
import tempfile
from typing import Iterator
import zipfile
import numpy as np
from pathlib import Path
from loguru import logger
from linc import get_config, write_nc_legacy
from linc.config.read import Config
from datetime import datetime as dt, time, timedelta, date

import psutil

from gfatpy.lidar.utils.utils import (
    get_532_from_telescope,
    licel_to_datetime,
    to_licel_date_str,
)
from gfatpy.utils.io import unzip_file
from gfatpy.lidar.utils.utils import LIDAR_INFO
from gfatpy.lidar.utils.utils import filter_wildcard
from gfatpy.lidar.nc_convert.utils import search_config_file
from gfatpy.lidar.utils.file_manager import info2general_path, info2path
from gfatpy.lidar.utils.types import LidarName, MeasurementType, Telescope
from gfatpy.utils.utils import parse_datetime

RAW_FIRST_LETTER = LIDAR_INFO["metadata"]["licel_file_wildcard"]


class Measurement:
    path: Path
    type: MeasurementType
    lidar_name: LidarName
    telescope: Telescope

    def __init__(
        self,
        path: Path,
        type: MeasurementType,
        lidar_name: str,
        telescope: str = "xf",
        **kwargs,
    ):
        self.path = path
        self.type = type
        self._is_zip = None
        self._filenames = None
        self.lidar_name = LidarName(lidar_name)
        self.telescope = Telescope(telescope)
        self._session_datetime = None
        self._datetimes = None
        self._unique_dates = None
        self._sub_dirs = None
        self._has_linked_dc = None
        self._linked_measurements = None
        self._dc = None        
        self._filepaths = None
        self.config = None
        self._unzipped_path = None

    @property
    def is_zip(self) -> bool:
        if self._is_zip is None:
            self._is_zip = self.path.suffix.endswith("zip")
        return self._is_zip

    @property
    def filenames(self) -> list[str]:
        if self._filenames is None:
            self._filenames = [file.name for file in self.get_filepaths()]
        return self._filenames

    @property
    def session_datetime(self) -> dt:
        if self._session_datetime is None:
            # Get datetime from filename RS_yyyymmdd_hhmm or RS_yyyymmdd_hhmm.zip
            self._session_datetime = dt.strptime(
                self.path.name.split(".")[0], f"{self.type.value}_%Y%m%d_%H%M"
            )
        return self._session_datetime

    @property
    def datetimes(self) -> list[dt]:
        """Get the dates from the measurement

        Returns:

            - list[dt]: List of dates
        """
        if self._datetimes is None:
            self._datetimes = [
                licel_to_datetime(file_.name)
                for file_ in sorted(list(self.get_filepaths()))
            ]
        return self._datetimes

    @property
    def unique_dates(self) -> list[date]:
        """Get the unique dates from the measurement

        Returns:

            - list[dt]: List of unique dates
        """
        if self._unique_dates is None:
            self._unique_dates = sorted(
                np.unique(
                    np.array([datetime_.date() for datetime_ in self.datetimes])
                ).tolist()
            )
        return self._unique_dates

    @property
    def sub_dirs(self) -> list[str]:
        """Extract sub-directories from the measurement path

        Returns:

            - list[str]: list of sub-directories.
        """
        if self._sub_dirs is None:
            folders = []
            path = self.path  # Store path in a local variable for use in the method
            if self.is_zip:
                with zipfile.ZipFile(path, "r") as zip_ref:
                    file_list = zip_ref.namelist()
                    folders = [
                        file.split("/")[-2] for file in file_list if file.endswith("/")
                    ]
            elif path.is_dir():
                folders = [f.name for f in path.iterdir() if f.is_dir()]
            self._sub_dirs = folders
        return self._sub_dirs

    @property
    def has_linked_dc(self) -> bool:
        """Check if the DC type measurement exists

        Returns:

            - bool: True if the DC type measurement exists. False otherwise.
        """
        if self._has_linked_dc is None:
            if self.type == MeasurementType.DC:
                self._has_linked_dc = False

            dc_path = self.path.parent / self.path.name.replace(
                self.type, MeasurementType.DC
            )
            self._has_linked_dc = dc_path.exists()
        return self._has_linked_dc

    @property
    def dc(self) -> "Measurement | None":
        """Get the DC type measurement

        Returns:

            - Measurement | None: DC type measurement
        """
        if self._dc is None:
            if self.has_linked_dc:
                self._dc = Measurement(
                    path=self.path.parent
                    / self.path.name.replace(self.type, MeasurementType.DC),
                    type=MeasurementType.DC,
                    lidar_name=self.lidar_name,
                )
        return self._dc

    @property
    def linked_measurements(
        self,
        number_of_previous_days: int = 1,
        raw_dir: str | Path | None = None,
    ) -> list["Measurement"] | None:
        """Add linked measurements to the measurement object.

        Args:

            - measurements (list): List of measurements.
        """
        # Add linked measurements to the measurement object
        # Linked measurements are measurements with the same date and type
        if self.type != MeasurementType.RS or self.type != MeasurementType.HF:
            return self._linked_measurements

        if isinstance(raw_dir, str):
            raw_dir = Path(raw_dir)
        elif raw_dir is None:
            # Split self.path by the first occurence of the lidar name
            raw_dir = self.path.parent.parent.parent.parent

        # Add previous days to the search
        prev_paths = self.__find_previous_paths(
            number_of_previous_days, self.lidar_name, raw_dir  # type: ignore
        )
        for prev_path in prev_paths:
            prev_measurements = []
            for path in prev_path.glob(f"{self.type.value}*"):
                new_measurement = Measurement(
                    path=path,
                    type=MeasurementType(path.name[:2]),
                    lidar_name=self.lidar_name,
                )
                # Check any self.unique_dates() is in new_measurement.unique_dates()
                if any(
                    date_ in new_measurement.unique_dates for date_ in self.unique_dates
                ):
                    prev_measurements.append(new_measurement)
        self._linked_measurements = prev_measurements
        return self._linked_measurements

    @property
    def unzipped_path(self) -> Path | None:        
        if self._unzipped_path is None:
            self._unzipped_path = self.unzip()
            if self._unzipped_path is not None:
                return Path(self._unzipped_path.name)
        else:
            return Path(self._unzipped_path.name)

    def unzip(
        self, pattern_or_list: str = r"\.\d+$", destination: Path | None = None
    ) -> tempfile.TemporaryDirectory | None:
        """Extract the zip file

        Args:

            - pattern_or_list (str, optional): pattern or list of patterns. Defaults to r'\\.\\d+$'.
            - destination (Path | None, optional): Directory to extract files. Defaults to None (extract to the same directory as the zip file).
        """
        if self.is_zip:
            if self._unzipped_path is None:
                self._unzipped_path = unzip_file(
                    self.path, pattern_or_list=pattern_or_list, destination=destination
                )
        else:
            self._unzipped_path = None
        return self._unzipped_path
    
    def get_config(self, config_dir) -> Config:
        # Get lidar configuration file
        config_filepath = search_config_file(
            self.lidar_name, self.session_datetime, config_dir
        )
        return get_config(config_filepath)

    def has_target_date(self, date: dt) -> bool:
        """Check if the measurement has the target date

        Args:

            - date (dt): Target date

        Returns:

            - bool: True if the measurement has the target date. False otherwise.
        """
        has_target_date = False
        for file in self.filenames:
            match = re.search(f"{RAW_FIRST_LETTER}{to_licel_date_str(date)}*", file)
            if match != None and match.span()[1] > 6:
                has_target_date = True
                break
        return has_target_date

    def generate_nc_output_path(
        self,
        target_date: dt | date,
        lidar_name: str,
        telescope: Telescope,
        measurement_type: MeasurementType | str,
        signal_type: MeasurementType | str,
        output_path: Path,
        subdir: str | None = None,
    ) -> Path:
        """Generate the output path for the netCDF file

        Args:

            - output_path (Path): Directory to save the netCDF file.
            - lidar_name (str): Lidar name.
            - telescope (Telescope): Telescope object (see gfatpy.lidar.nc_convert.types.Telescope).
            - measurement_type (MeasurementType): Measurement type (eg., RS, DC, etc.).
            - signal_type (str): Signal type.

        Returns:

            - Path: Output path for the netCDF file.
        """
        if isinstance(measurement_type, str):
            measurement_type = MeasurementType(measurement_type)

        if isinstance(signal_type, str):
            signal_type = MeasurementType(signal_type)
        
        return info2path(
            lidar_name=lidar_name,
            channel=get_532_from_telescope(telescope),
            measurement_type=measurement_type.value,
            signal_type=signal_type.value,
            date=target_date,
            dir=output_path,
            subdir=subdir,
        )

    def __find_previous_paths(
        self, number_of_previous_days: int, lidar_name: LidarName, raw_dir: Path
    ) -> list[Path]:
        """Find the paths for the previous days

        Args:

             number_of_previous_days (int): Number of previous days to look for.
             lidar_name (LidarName): Lidar name (see gfatpy.lidar.nc_convert.types.LidarName).
             raw_dir (Path): Directory for the raw data.

        Returns:

             list[Path]: List of paths for the previous days.
        """
        current_date = sorted(self.unique_dates)[0]
        prev_paths = [
            info2general_path(
                lidar_name.value,
                date=current_date - timedelta(days=n_day),
                data_dir=raw_dir,
            )
            for n_day in range(1, number_of_previous_days + 1)
        ]
        # Remove paths that do not exist
        previous_paths = [prev_path for prev_path in prev_paths if prev_path.exists()]
        return previous_paths

    def __get_current_filepaths(
        self,
        pattern_or_list: str = r"\.\d+$",
        within_period: tuple[dt, dt] | None = None,
    ) -> set[Path]:
        """Get the files from a measurement

        Args:

            - measurement (Measurement): Measurement object

        Returns:

            - set[Path]: Set of licel files
        """

        # Get files from the measurement main path
        if self.is_zip:
            dir_ = self.unzipped_path
        else:
            dir_ = self.path        
        if dir_ is None:
            raise Exception(
                f"No files found in {self.path} to meet the wildcard {pattern_or_list}"
            )

        found_files = set(filter_wildcard(dir_))

        if within_period is not None:
            date_ini, date_end = within_period
            selected_filepaths = {
                licel_
                for licel_ in found_files
                if date_ini <= licel_to_datetime(licel_.name) <= date_end
            }
        else:
            selected_filepaths = found_files
        return selected_filepaths

    def get_filepaths(
        self,
        pattern_or_list: str = r"\.\d+$",
        within_period: tuple[dt, dt] | None = None,
    ) -> set[Path]:

        filepaths = self.__get_current_filepaths(
            pattern_or_list=pattern_or_list, within_period=within_period
        )
        if self.linked_measurements is not None:
            for measurement in self.linked_measurements:
                filepaths.update(
                    measurement.__get_current_filepaths(
                        pattern_or_list=pattern_or_list, within_period=within_period
                    )
                )
        return filepaths

    def to_nc(
        self,
        target_date: dt | date | str | None = None,
        output_dir: str | Path | None = None,
        config_dir: str | Path | None = None,
        within_period: tuple[dt, dt] | None = None,
    ) -> None:

        if isinstance(output_dir, str):
            output_dir = Path(output_dir)
        elif output_dir is None:
            output_dir = Path.cwd()

        if target_date is None:
            target_date = self.session_datetime
        
        if isinstance(target_date, str):
            target_datetime = parse_datetime(target_date)
            target_date = target_datetime.date()
        elif isinstance(target_date, dt):
            target_datetime = target_date
            target_date = target_datetime.date()
        elif isinstance(target_date, date):
            target_datetime = dt.combine(target_date, time(0, 0))
            target_date = target_date

        if not target_date in self.unique_dates and self.type != MeasurementType.DC:            
            raise ValueError(
                f"Target datetime {target_date} not found in the measurement dates {self.unique_dates}"
            )

        # Get lidar configuration file
        config = self.get_config(config_dir=config_dir)

        if self.type == MeasurementType.RS or self.type == MeasurementType.HF:
            result_path = self.generate_nc_output_path(
                target_date=target_date,
                lidar_name=self.lidar_name,
                telescope=self.telescope,
                measurement_type=self.type,
                signal_type=MeasurementType.RS,
                output_path=output_dir,
            )
            if within_period is None:
                files2convert = self.get_filepaths()
            else:
                files2convert = self.get_filepaths(within_period=within_period)

            if len(files2convert) != 0:
                # Generate the output path
                result_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Writing {result_path.name}")

                # Write the nc file
                try:
                    write_nc_legacy(files2convert, result_path, config=config)
                except Exception as e:
                    raise Exception(f"Error writing {result_path}: {e}")
        elif self.type == MeasurementType.DC:

            result_path = self.generate_nc_output_path(
                target_date=self.session_datetime,
                lidar_name=self.lidar_name,
                telescope=self.telescope,
                measurement_type=self.type,
                signal_type=MeasurementType.RS,
                output_path=output_dir,
            )
            files2convert = self.get_filepaths()
            if len(files2convert) != 0:
                result_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Writing {result_path.name}")

                # Write the nc file
                try:
                    write_nc_legacy(files2convert, result_path, config=config)
                except Exception as e:
                    raise Exception(f"Error writing {result_path}: {e}")
        else:
            for subdir in self.sub_dirs:
                if subdir == self.unique_dates[0].strftime("%Y%m%d"):
                    continue
                try:
                    escaped_subdir = re.escape(subdir)
                    files2convert = self.get_filepaths(
                        pattern_or_list=rf".*{escaped_subdir}.*"
                    )
                except:
                    raise RuntimeError(f"Error in {self.path}")
                if len(files2convert) != 0:
                    result_path = self.generate_nc_output_path(
                        target_date=self.session_datetime,
                        lidar_name=self.lidar_name,
                        telescope=self.telescope,
                        measurement_type=self.type,
                        signal_type=MeasurementType.RS,
                        output_path=output_dir,
                        subdir=subdir,
                    )
                    result_path.parent.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Writing {result_path.name}")

                    # Write the nc file
                    try:
                        write_nc_legacy(files2convert, result_path, config=config)
                    except Exception as e:
                        raise Exception(f"Error writing {result_path}: {e}")
        return None

    def remove_tmp_unzipped_dir(self):
        """Delete temporary folders created during the process.

        Raises:

            - OSError: If there is an error deleting the temporary folder.
        """ 
        if self._unzipped_path is not None:
            try:
                self._unzipped_path.cleanup()                    
                logger.info(f"Temporary folder deleted: {self.unzipped_path}")
            except:
                logger.error(f"Error deleting temporary folder: {self.unzipped_path}")


    def __str__(self):
        return f"Measurement Object\nPath: {self.path}\nType: {self.type}\nUnique dates: {self.unique_dates}\nIs ZIP: {self.is_zip}\nFiles: {self.filenames}\nSub-directories: {self.sub_dirs}\nDC Path: {self.dc}\nHas DC: {self.has_linked_dc}\nUnzipped Path: {self.unzipped_path}\n\nLinked Measurements: {self.linked_measurements}\n"


def to_measurements(lidar_name: str, glob: Iterator[Path]) -> list[Measurement]:
    """Converts a list of paths to a list of Measurement objects.

    Args:

        - glob (Iterator[Path]): Iterator of paths to convert.

    Returns:

        - list[Measurement]: List of Measurement objects.
    """
    measurements = []
    for path in glob:
        new_measurement = Measurement(
            type=MeasurementType(path.name[:2]),
            path=path,
            lidar_name=lidar_name,
        )
        measurements.append(new_measurement)
    return measurements


def filter_by_type(
    measurements: list[Measurement], mtype: MeasurementType
) -> list[Measurement]:
    """Filter a list of measurements by type.

    Args:

        - measurements (list[Measurement]): List of measurements to filter.
        - mtype (MeasurementType): Type to filter by.

    Returns:

        - list[Measurement]: Filtered list of measurements.
    """
    return list(
        filter(
            lambda m: m.type == mtype,
            measurements,
        )
    )
