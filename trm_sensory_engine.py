import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class TRMSensoryEngine:
    def __init__(self, lmbda: float, tau: float, rho: float):
        """
        TIMDR TRM Sensory Engine (prawdziwy TRM-kształt).
        λ (lmbda) - skala geometryczno-polowa (rozpiętość drabiny)
        τ (tau)   - czas wewnętrzny / taktowanie ewolucji
        ρ (rho)   - gęstość skrętu polowego (TRM-density)
        """
        self.lmbda = lmbda
        self.tau = tau
        self.rho = rho

    def generate_trm_field(self, resolution: int = 2000):
        """
        Generuje TRM-kształt jako pole:
        - oś T: czas wewnętrzny TIMDR (nie zwykły czas)
        - helisa zewnętrzna: nośnik pola (flux line)
        - helisa wewnętrzna: implozja / collapse
        - gęstość: lokalna wartość TRM-density (ρ_eff)
        """
        # Oś ewolucji (TIMDR-time, nie czas fizyczny)
        T = np.linspace(0, 2 * np.pi * self.tau, resolution)

        # TRM-phase: faza skrętu polowego (nie sinus geometryczny)
        phase = self.rho * T

        # Lokalna gęstość pola (TRM-density) – nie amplituda, tylko "zagęszczenie"
        density = 0.5 * (1.0 + np.sin(phase))  # w [0,1], naturalny próg 0.5

        # Kolaps TIMDR: wszystko poniżej 0.5 traktujemy jako "implozję"
        collapse_mask = density < 0.5
        stable_mask = ~collapse_mask

        # Promień zewnętrznej nici pola (flux line) – reaguje na gęstość
        radius_outer = self.lmbda * (0.7 + 0.6 * density)

        # Promień wewnętrznej nici (implozja) – odwrotność gęstości
        radius_inner = self.lmbda * (0.3 + 0.4 * (1.0 - density))

        # Z-Drabina: nie wysokość, tylko "poziom ewolucji" (TIMDR-ladder)
        Z = (T / (2 * np.pi)) * (self.lmbda * self.rho)

        # Nici zewnętrzna (nośnik pola)
        X_outer = radius_outer * np.cos(T)
        Y_outer = radius_outer * np.sin(T)

        # Nici wewnętrzna (implozja / collapse)
        X_inner = radius_inner * np.cos(T + np.pi / 2.0)
        Y_inner = radius_inner * np.sin(T + np.pi / 2.0)

        return {
            "T": T,
            "Z": Z,
            "density": density,
            "collapse_mask": collapse_mask,
            "stable_mask": stable_mask,
            "X_outer": X_outer,
            "Y_outer": Y_outer,
            "X_inner": X_inner,
            "Y_inner": Y_inner,
        }

    def render_visual(self):
        """
        Wizualizacja TRM-kształtu:
        - zewnętrzna nić: stabilne pole (stable_mask)
        - wewnętrzna nić: implozja (collapse_mask)
        - kolor: lokalna gęstość TRM (ρ_eff)
        """
        field = self.generate_trm_field()

        Xo = field["X_outer"]
        Yo = field["Y_outer"]
        Zo = field["Z"]
        Xi = field["X_inner"]
        Yi = field["Y_inner"]
        Zi = field["Z"]
        density = field["density"]
        collapse_mask = field["collapse_mask"]
        stable_mask = field["stable_mask"]

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Zewnętrzna nić pola – tylko stabilne fragmenty (density >= 0.5)
        ax.plot(
            Xo[stable_mask],
            Yo[stable_mask],
            Zo[stable_mask],
            label='TRM Stable Flux Line',
            color='cyan',
            linewidth=2.5,
            zorder=2
        )

        # Wewnętrzna nić – obszary kolapsu (density < 0.5)
        ax.plot(
            Xi[collapse_mask],
            Yi[collapse_mask],
            Zi[collapse_mask],
            label='TRM Collapse Core',
            color='magenta',
            linewidth=1.8,
            zorder=3
        )

        # Gęstość jako chmura punktów (pole, nie geometria)
        scatter =
