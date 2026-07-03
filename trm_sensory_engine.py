import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class TRMSensoryEngine:
    def __init__(self, lmbda: float, tau: float, rho: float):
        """
        Inicjalizacja silnika zmysłowego TIMDR.
        λ (lmbda) - skala geometryczna
        τ (tau)   - częstotliwość bazowa rezonansu / czas
        ρ (rho)   - gęstość informacyjna (złożoność amplitudy)
        """
        self.lmbda = lmbda
        self.tau = tau
        self.rho = rho

    def generate_topological_wave(self, resolution: int = 500):
        """Generuje geometrię skrętu polowego (TRM-Geometry-Core) dla obrazu."""
        theta = np.linspace(0, 2 * np.pi, resolution)
        phi = np.linspace(0, 2 * np.pi, resolution)
        THETA, PHI = np.meshgrid(theta, phi)
        
        # Wprowadzenie skrętu topologicznego wymuszonego przez ρ i τ
        twist = self.rho * np.sin(self.tau * THETA)
        
        # Geometria pola - odwzorowanie toroidalne zmienione skrętem (TRM)
        R = 2 + np.cos(PHI + twist) * self.lmbda
        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        Z = np.sin(PHI + twist) * self.lmbda
        
        return X, Y, Z

    def render_visual(self):
        """Wyświetla trójwymiarową strukturę fali topologicznej."""
        X, Y, Z = self.generate_topological_wave()
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Kolorowanie powierzchni gęstością pola (ρ)
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none', alpha=0.85)
        
        ax.set_title(f"TIMDR Visual Field Manifestation\n[λ={self.lmbda}, τ={self.tau}, ρ={self.rho}]", fontsize=12)
        ax.axis('off') # Ukrywamy osie, liczy się czysta geometria pola
        plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Field Density (Rho)')
        plt.show()

    def generate_resonance_sound(self, duration: float = 3.0, sample_rate: int = 44100):
        """Generuje czysty rezonans dźwiękowy (TIMDR Transduction) bez strat energii."""
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        # Częstotliwość bazowa uwarunkowana parametrem rezonansu τ
        base_freq = 220 * self.tau  
        
        # Fala podstawowa (implozja/ssanie) + wyższe harmoniczne wymuszone gęstością ρ (skręt)
        wave = np.sin(2 * np.pi * base_freq * t)
        
        # Dodanie harmonicznych punktu zwrotnego (stabilność rezonansu)
        for i in range(2, 5):
            wave += (self.rho / i) * np.sin(2 * np.pi * (base_freq * i) * t * (1 / (t + 1)**(self.lmbda)))

        # Normalizacja audio do formatu 16-bit PCM
        wave = wave / np.max(np.abs(wave))
        audio_data = np.int16(wave * 32767)
        
        filename = f"trm_resonance_L{self.lmbda}_T{self.tau}_R{self.rho}.wav"
        wavfile.write(filename, sample_rate, audio_data)
        print(f"[PC_TIMDR Output]: Dźwięk wyemitowany i zapisany jako {filename}")

# --- URUCHOMIENIE WALIDACYJNE I GENEROWANIE ---
if __name__ == "__main__":
    # Konfiguracja wektora stanu: Średnia skala, wysoki rezonans, gęsty skręt topologiczny
    engine = TRMSensoryEngine(lmbda=0.8, tau=5.0, rho=1.5)
    
    # 1. Wyemituj obraz (Manifestacja Wizualna)
    engine.render_visual()
    
    # 2. Wyemituj dźwięk (Manifestacja Akustyczna)
    engine.generate_resonance_sound()
