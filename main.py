"""
Undersøgelse af sammenhængen mellem DVR90, DKLAT og DKMSL
"""

from dataclasses import dataclass

import fiona
import pyproj

TIMESPAN = 2023 - 1990

# Brug PROJ til at aflæse modelværdier
DVR90 = pyproj.Transformer.from_pipeline(
    "proj=vgridshift +grids=./dk_sdfe_dvr90.tif +multiplier=1"
)
DKLAT = pyproj.Transformer.from_pipeline(
    "proj=vgridshift +grids=./dklat_2022.tif +multiplier=1"
)
DKMSL = pyproj.Transformer.from_pipeline(
    "proj=vgridshift +grids=./dkmsl_2022.tif +multiplier=1"
)
REL_UPLIFT = pyproj.Transformer.from_pipeline(
    "proj=vgridshift +grids=./rel.tif +multiplier=1"
)

SCHEMA = {
    "geometry": "Point",
    "properties": dict(
        [
            ("e_dvr90", "float"),
            ("e_lmsl1990", "float"),
            ("e_dklat", "float"),
            ("e_dkmsl", "float"),
            ("delta_msl", "float"),
            ("relative_uplift", "float"),
            ("dtu_lat", "float"),
            ("dmi_lat", "float"),
            ("lat_diff", "float"),
        ]
    ),
}


@dataclass
class Station:
    """
    Properties der starter med "E" angiver de forskellige referencefladers
    ellipsoidehøjder på stationens placering.
    """

    name: str
    coordinate: tuple
    dmi_lat: float
    dvr90_msl_offset: float  # DVR90 kote for MSL i 1990
    dvr90_rel_uplift: float  # Relativ uplift ifølge Klaus Schmidt, DVR90 publikation

    timespan: int = 2023 - 1990

    def feature(self) -> dict:
        """
        Returner feature til skrivning med fiona.

        Følger SCHEMA.
        """
        return {
            "geometry": {
                "type": "Point",
                "coordinates": self.coordinate[0:2],
            },
            "properties": {
                "e_dvr90": self.E_DVR90,
                "e_lmsl1990": self.E_LMSL1990,
                "e_dklat": self.E_DKLAT,
                "e_dkmsl": self.E_DKMSL,
                "delta_msl": self.ΔMSL,
                "relative_uplift": self.relative_uplift,
                "dtu_lat": self.model_lat,
                "dmi_lat": self.dmi_lat,
                "lat_diff": self.dmi_lat - self.model_lat,
            },
        }

    @property
    def E_DVR90(self) -> float:
        return DVR90.transform(*self.coordinate)[2]

    @property
    def E_LMSL1990(self) -> float:
        return self.E_DVR90 + self.dvr90_msl_offset * 0.01

    @property
    def E_DKLAT(self) -> float:
        return DKLAT.transform(*self.coordinate)[2]

    @property
    def ΔMSL(self) -> float:
        return self.E_LMSL1990 - self.E_DKMSL

    @property
    def E_DKMSL(self) -> float:
        return DKMSL.transform(*self.coordinate)[2]

    @property
    def relative_uplift(self) -> float:
        return REL_UPLIFT.transform(*self.coordinate)[2] / 1000 * self.timespan

    @property
    def model_lat(self) -> float:
        return self.E_DKLAT - self.E_DKMSL


STATIONS = [
    Station("Esbjerg", (8.43333, 55.46667, 0), -1.208, 4.6, -1.08),
    Station("Fredericia", (9.75000, 55.56667, 0), -0.255, -0.4, -0.95),
    Station("Frederikshavn", (10.55000, 57.43333, 0), -0.271, -6.0, 0.51),
    Station("Gedser", (11.91667, 54.56667, 0), -0.097, 5.2, -0.93),
    Station("Hirtshals", (9.96667, 57.6, 0), -0.23, -7.9, 0.41),
    Station("Hornbæk", (12.45000, 56.10000, 0), -0.157, 0.1, -0.06),
    Station("Korsør", (11.15000, 55.33333, 0), -0.238, 2.6, -0.63),
    Station("København", (12.60000, 55.70000, 0), -0.147, 4.1, -0.23),
    Station("Slipshavn", (10.83333, 55.28333, 0), -0.275, 0.0, -0.79),
    Station("Aarhus", (10.21667, 56.15000, 0), -0.331, -1.0, -0.46),
]

for station in STATIONS:
    print(f"{station.name}")
    print(f"  E_DVR90    = {station.E_DVR90:.4f}")
    print(f"  E_LMSL1990 = {station.E_LMSL1990:.4f}")
    print(f"  E_DKMSL    = {station.E_DKMSL:.4f}")
    print(f"  E_DKLAT    = {station.E_DKLAT:.4f}")
    print("")
    print(f"  DKLAT-DVR90    = {station.E_DKLAT-station.E_DVR90:.4f}")
    print(f"  DKMSL-DVR90    = {station.E_DKMSL-station.E_DVR90:.4f}")
    print(f"  LAT: DMI       = {station.dmi_lat:.4f}")
    print(f"       DTU       = {station.model_lat:.4f}")
    print(f"       DMI-DTU   = {station.dmi_lat-station.model_lat:.4f}")
    print("")
    print(f"  ΔMSL           = {station.ΔMSL:.4f}")
    print(f"  ΔMSL-RelUplift = {station.ΔMSL-station.relative_uplift:.4f}")
    print(f"  RelUplift      = {station.relative_uplift:.4f}")
    print()

# skriv geojson fil
with fiona.open("LAT.geojson", "w", driver="GeoJSON", schema=SCHEMA) as geojson:
    for station in STATIONS:
        geojson.write(station.feature())
