from collections import OrderedDict
from math import ceil

import numpy as np
from numba import float64
from numba.experimental import jitclass

model_spec = OrderedDict()
# Scales and dimensionless parameters as arrays, one for each grain size
model_spec["SettlingScale"] = float64[::1]  # Settling speed
model_spec["Velocity_ratio"] = float64[::1]  # wind speed/settling speed
# model_spec["xyScale"] = float64[::1]  # Horizontal scale
model_spec["xScale"] = float64[::1]  # Easting scale
model_spec["yScale"] = float64[::1]  # Northing scale
model_spec["Lx"] = float64[::1]  # Dimensionless extent in x
model_spec["Ly"] = float64[::1]  # Dimensionless extent in y
model_spec["cScale"] = float64[::1]  # Concentration
model_spec["QScale"] = float64[::1]  # Source term
model_spec["Peclet_number"] = float64  # Peclet number
model_spec["Diffusion_ratio"] = float64  # Kappa_h/Kappa_v
model_spec["sigma_hat"] = float64[::1]  # source radius/xyScale
model_spec["sigma_hat_scale"] = float64[::1]  # sigma_hat scaled to -pi->pi


@jitclass(model_spec)
class ModelParameters:

    # pylint: disable=too-many-instance-attributes
    # These attributes are all needed in ModelParameters

    def __init__(self):
        self.SettlingScale = np.empty((1), dtype=np.float64)
        self.SettlingScale[:] = np.nan
        self.Velocity_ratio = np.empty((1), dtype=np.float64)
        self.Velocity_ratio[:] = np.nan
        # self.xyScale = np.empty((1), dtype=np.float64)
        # self.xyScale[:] = np.nan
        self.xScale = np.empty((1), dtype=np.float64)
        self.xScale[:] = np.nan
        self.yScale = np.empty((1), dtype=np.float64)
        self.yScale[:] = np.nan
        self.Lx = np.empty((1), dtype=np.float64)
        self.Lx[:] = np.nan
        self.Ly = np.empty((1), dtype=np.float64)
        self.Ly[:] = np.nan
        self.cScale = np.empty((1), dtype=np.float64)
        self.cScale[:] = np.nan
        self.QScale = np.empty((1), dtype=np.float64)
        self.QScale[:] = np.nan
        self.Peclet_number = np.nan
        self.Diffusion_ratio = np.nan
        self.sigma_hat = np.empty((1), dtype=np.float64)
        self.sigma_hat[:] = np.nan
        self.sigma_hat_scale = np.empty((1), dtype=np.float64)
        self.sigma_hat_scale[:] = np.nan

    # def from_params(
    #     self, solver_params, met_params, source_params, grain_params, physical_params, met,
    # ):
    def from_params(
        self, params, xScale, yScale,
    ):
        solver_params = params.solver
        met_params = params.met
        source_params = params.source
        grain_params = params.grains
        physical_params = params.physical
        
        N = met_params.Ws_scale.shape[0]
        self.SettlingScale = np.empty((N), dtype=np.float64)
        self.Velocity_ratio = np.empty((N), dtype=np.float64)
        # self.xyScale = np.empty((N), dtype=np.float64)
        self.xScale = np.empty((N), dtype=np.float64)
        self.yScale = np.empty((N), dtype=np.float64)
        self.Lx = np.empty((N), dtype=np.float64)
        self.Ly = np.empty((N), dtype=np.float64)
        self.cScale = np.empty((N), dtype=np.float64)
        self.QScale = np.empty((N), dtype=np.float64)
        self.sigma_hat = np.empty((N), dtype=np.float64)
        self.sigma_hat_scale = np.empty((N), dtype=np.float64)

        self.Peclet_number = (
            physical_params.Kappa_h / met_params.U_scale / source_params.PlumeHeight
        )
        self.Diffusion_ratio = physical_params.Kappa_h / physical_params.Kappa_v
        for j in range(N):
            self.SettlingScale[j] = met_params.Ws_scale[j]
            self.Velocity_ratio[j] = met_params.U_scale / self.SettlingScale[j]
            # self.xyScale[j] = (
            #     met_params.U_scale * source_params.PlumeHeight / self.SettlingScale[j]
            # )

            #z, xy = settle_grain(params,met,j,source_params.PlumeHeight)
            self.xScale[j] = xScale[j] #np.max(np.abs(xy[0,:]))
            self.yScale[j] = yScale[j] #np.max(np.abs(xy[1,:]))

            # self.Lx[j] = (
            #     ceil(3 * source_params.radius / self.xyScale[j]) * solver_params.domX
            # )
            # self.Ly[j] = (
            #     ceil(3 * source_params.radius / self.xyScale[j]) * solver_params.domY
            # )
            self.Lx[j] = (
                ceil(3 * source_params.radius / self.xScale[j]) * solver_params.domX
            )
            self.Ly[j] = (
                ceil(3 * source_params.radius / self.yScale[j]) * solver_params.domY
            )
            self.cScale[j] = (
                grain_params.proportion[j]
                * source_params.MER
                / source_params.radius**2
                / self.SettlingScale[j]
            )
            self.QScale[j] = grain_params.proportion[j] * source_params.MER
            # self.sigma_hat[j] = source_params.radius / self.xyScale[j]
            self.sigma_hat[j] = source_params.radius / np.maximum(self.xScale[j], self.yScale[j])
            self.sigma_hat_scale[j] = (
                np.pi
                * self.sigma_hat[j]
                / np.sqrt(solver_params.domX * solver_params.domY)
            )

    def from_values(
        self,
        SettlingScale,
        Velocity_ratio,
        # xyScale,
        xScale,
        yScale,
        Lx,
        Ly,
        cScale,
        QScale,
        Peclet_number,
        Diffusion_ratio,
        sigma_hat,
        sigma_hat_scale,
    ):
        self.SettlingScale = SettlingScale
        self.Velocity_ratio = Velocity_ratio
        # self.xyScale = xyScale
        self.xScale = xScale
        self.yScale = yScale
        self.Lx = Lx
        self.Ly = Ly
        self.cScale = cScale
        self.QScale = QScale
        self.Peclet_number = Peclet_number
        self.Diffusion_ratio = Diffusion_ratio
        self.sigma_hat = sigma_hat
        self.sigma_hat_scale = sigma_hat_scale

    def describe(self):
        print("Model parameters for AshDisperse")
        print("  Settling speed scale = ", self.SettlingScale)
        print("  Velocity ratio = ", self.Velocity_ratio)
        print("  concentration scale = ", self.cScale)
        # print("  x and y scale = ", self.xyScale)
        print("  x scale = ", self.xScale)
        print("  y scale = ", self.yScale)
        print("  Lx = ", self.Lx)
        print("  Ly = ", self.Ly)
        print("  source flux scale = ", self.QScale)
        print("  Peclet number = ", self.Peclet_number)
        print("  Diffusion ratio = ", self.Diffusion_ratio)
        print("********************")


# pylint: disable=E1101
ModelParameters_type = ModelParameters.class_type.instance_type
