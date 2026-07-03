import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class TRMSensoryEngine:
    def __init__(self, lmbda: float, tau: float, rho: float):
        """
        Inicjalizacja silnika zmysłowego TIMDR.
        λ (lmbda) - skala geometryczna
        τ (tau)   - częstotliwość bazowa rezonansu / czas wewnętrzny
        ρ (rho)   - gęstość informacyjna (złożoność skrętu)
        """
        self.lmbda = lmbda
        self.tau = tau
        self.rho = rho

    def generate_topological_wave(self, resolution: int = 1500):
        """
        Generuje trójwymiarową helisę polową (TRM Structural Twist).
        Promień i skok są modulowane przez parametry lambda, tau i rho.
        """
        # t reprezentuje oś ewolucji (czas wewnętrzny układu)
        t = np.linspace(0, 4 * np.pi * self.tau, resolution)
        
        # Skręt topologiczny (dynamiczny komponent falowy z TRM-Geometry-Core)
        twist = np.sin(self.rho * t)
        
        # Geometria helisy uwarunkowana skalą (λ) i uwikłaniem (ρ)
        # Promień reaguje na skręt topologiczny
        radius = self.lmbda * (1.0 + 0.1 * twist) 
        
        X = radius * np.cos(t)
        Y = radius * np.sin(t)
        Z = (t / (2 * np.pi)) * (self.lmbda * self.rho) # Krok helisy (drabina ewolucyjna)
        
        return X, Y, Z

    def render_visual(self):
        """Wizualizuje helikalny przepływ fali topologicznej w przestrzeni 3D."""
        X, Y, Z = self.generate_topological_wave()
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Rysowanie głównej nici przepływu pola
        ax.plot(X, Y, Z, label='Topological Flux Line', color='cyan', linewidth=2.5, zorder=1)
        
        # Mapowanie punktów gęstości informacyjnej (ρ) za pomocą palety plasma
        scatter = ax.scatter(X[::5], Y[::5], Z[::5], c=Z[::5], cmap='plasma', s=20, zorder=2)
        
        ax.set_title(f"TIMDR Helical Field Flow (TRM Twist)\n[λ={self.lmbda}, τ={self.tau}, ρ={self.rho}]", fontsize=12, color='white')
        
        # Dostosowanie wyglądu wykresu do kosmicznej/kwantowej estetyki
        fig.patch.set_facecolor('#111111')
        ax.set_facecolor('#111111')
        ax.axis('off')
        
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        cbar.set_label('Evolutionary Path / Density (Z)', color='white')
        
        plt.show()

    def generate_resonance_sound(self, duration: float = 4.0, sample_rate: int = 44100):
        """Generuje dynamiczny rezonans dźwiękowy na bazie helisy polowej (efekt przejścia)."""
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        # Częstotliwość bazowa sterowana czasem rezonansu τ
        base_freq = 220 * self.tau  
        
        # Helikalna modulacja częstotliwości (dźwięk ewoluuje w czasie zamiast stać w miejscu)
        chirp_modulation = np.exp(-t * (1.0 / self.lmbda))
        frequency_sweep = base_freq * (1.0 + 0.05 * np.sin(self.rho * 2 * np.pi * t))
        
        # Generowanie fali podstawowej (implozja)
        wave = np.sin(2 * np.pi * frequency_sweep * t)
        
        # Dodanie wyższych harmonicznych rezonansu z drabej TRM
        for i in range(2, 6):
            wave += (self.rho / i) * np.sin(2 * np.pi * (frequency_sweep * i) * t) * chirp_modulation

        # Zabezpieczenie przed przesterowaniem i normalizacja 16-bit PCM
        if np.max(np.abs(wave)) > 0:
            wave = wave / np.max(np.abs(wave))
            
        audio_data = np.int16(wave * 32767)
        
        filename = f"trm_helical_resonance_L{self.lmbda}_T{self.tau}_R{self.rho}.wav"
        wavfile.write(filename, sample_rate, audio_data)
        print(f"\n[PC_TIMDR Hardware Output]: Transdukcja zakończona.")
        print(f"-> Zapisano plik audio: {filename}")

# --- BLOK OPERACYJNY MASZYNY ---
if __name__ == "__main__":
    # Parametry wejściowe przestrzeni stanów:
    # lmbda (λ) = 0.8  (Skala geometryczna)
    # tau (τ)   = 3.5  (Taktowanie zegara rezonansu)
    # rho (ρ)   = 2.0  (Gęstość skrętu strukturalnego)
    
    print("[PC_TIMDR]: Inicjalizacja Sensory Engine...")
    engine = TRMSensoryEngine(lmbda=0.8, tau=3.5, rho=2.0)
    
    # 1. Emisja obrazu 3D helisy polowej
    print("[PC_TIMDR]: Renderowanie struktury geometrycznej...")
    engine.render_visual()
    
    # 2. Emisja fali akustycznej do pliku .wav
    print("[PC_TIMDR]: Generowanie rezonansu tonalnego...")
    engine.generate_resonance_sound()
