import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import HTML

mpl.rcParams['animation.embed_limit'] = 100

class ManufacturingMachine:
    def __init__(self, initial_temp, max_temp, optimal_temp, initial_production_rate, initial_power):
        self.temperature = initial_temp
        self.max_temp = max_temp
        self.optimal_temp = optimal_temp
        self.production_rate = initial_production_rate
        self.power_consumption = initial_power
        self.pressure = 1.0
        self.stress = 1.0

    def update(self):
        self.temperature += np.random.normal(0, 2)
        self.temperature = np.clip(self.temperature, 0, self.max_temp)
        temp_factor = 1 - abs(self.temperature - self.optimal_temp) / self.optimal_temp
        self.production_rate = max(0, self.production_rate * temp_factor + np.random.normal(0, 0.5))
        self.power_consumption += np.random.normal(0, 0.2)
        self.power_consumption = np.clip(self.power_consumption, 0, 100)
        self.pressure += np.random.normal(0, 0.1)
        self.stress += np.random.normal(0, 0.05)

class DigitalTwin:
    def __init__(self, machine):
        self.machine = machine
        self.time = []
        self.temp_history = []
        self.prod_history = []
        self.power_history = []
        self.pressure_history = []
        self.stress_history = []
        self.rotation = 0

    def update(self, frame):
        self.machine.update()
        self.time.append(frame)
        self.temp_history.append(self.machine.temperature)
        self.prod_history.append(self.machine.production_rate)
        self.power_history.append(self.machine.power_consumption)
        self.pressure_history.append(self.machine.pressure)
        self.stress_history.append(self.machine.stress)

        self.rotation += self.machine.production_rate * 5
        self.rotation %= 360

        self.temp_line.set_data(self.time, self.temp_history)
        self.prod_line.set_data(self.time, self.prod_history)
        self.power_line.set_data(self.time, self.power_history)
        self.pressure_line.set_data(self.time, self.pressure_history)
        self.stress_line.set_data(self.time, self.stress_history)

        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()
        self.ax4.relim()
        self.ax4.autoscale_view()
        self.ax5.relim()
        self.ax5.autoscale_view()

        self.ax6.clear()
        self.ax6.set_xlim(-2, 2)
        self.ax6.set_ylim(-2, 2)
        self.ax6.set_zlim(-2, 2)
        self.ax6.set_box_aspect((1, 1, 1))
        self.ax6.set_axis_off()

        num_blades = 12
        blade_lengths = [1.0, 1.5, 2.0]
        blade_widths = [0.3, 0.5, 0.7]
        hub_radius = 0.2
        hub_length = 1.0
        angle_offset = np.radians(self.rotation)
        blade_y_positions = [-0.75, 0, 0.75]  # Blades along the y-axis

        # Hub structure along the y-axis
        Z_hub = np.ones(100) * hub_radius
        Y_hub = np.linspace(-hub_length / 2, hub_length / 2, 100)
        X_hub = np.zeros_like(Y_hub)
        self.ax6.plot_surface(np.array([X_hub, X_hub]), np.array([Y_hub, Y_hub]),
                              np.array([Z_hub, -Z_hub]), color='gray', alpha=0.8)

        for idx, y_pos in enumerate(blade_y_positions):
            blade_length = blade_lengths[idx]
            blade_width = blade_widths[idx]
            theta = np.linspace(0, np.pi, 50)
            r_blade = blade_length * (1 - np.cos(theta))

            for i in range(num_blades):
                blade_angle = i * 2 * np.pi / num_blades + angle_offset
                Z_blade = r_blade * np.cos(blade_angle) + hub_radius * np.cos(blade_angle)
                X_blade = r_blade * np.sin(blade_angle) + hub_radius * np.sin(blade_angle)
                Y_blade = np.linspace(y_pos - blade_width / 2, y_pos + blade_width / 2, len(Z_blade))

                self.ax6.plot_surface(np.array([X_blade, X_blade]),
                                      np.array([Y_blade, Y_blade]),
                                      np.array([Z_blade, Z_blade[::-1]]),
                                      color='silver', alpha=0.8)

        self.ax6.text2D(0.05, 0.95, f"Temp: {self.machine.temperature:.2f}", transform=self.ax6.transAxes)
        self.ax6.text2D(0.05, 0.90, f"Prod: {self.machine.production_rate:.2f}", transform=self.ax6.transAxes)
        self.ax6.text2D(0.05, 0.85, f"Power: {self.machine.power_consumption:.2f}W", transform=self.ax6.transAxes)
        self.ax6.text2D(0.05, 0.80, f"Pressure: {self.machine.pressure:.2f}", transform=self.ax6.transAxes)
        self.ax6.text2D(0.05, 0.75, f"Stress: {self.machine.stress:.2f}", transform=self.ax6.transAxes)

        return self.temp_line, self.prod_line, self.power_line, self.pressure_line, self.stress_line

    def visualize(self):
        fig = plt.figure(figsize=(15, 15))
        self.ax1 = fig.add_subplot(321)
        self.ax2 = fig.add_subplot(322)
        self.ax3 = fig.add_subplot(323)
        self.ax4 = fig.add_subplot(324)
        self.ax5 = fig.add_subplot(325)
        self.ax6 = fig.add_subplot(326, projection='3d')

        self.temp_line, = self.ax1.plot([], [], lw=2)
        self.prod_line, = self.ax2.plot([], [], lw=2, color='r')
        self.power_line, = self.ax3.plot([], [], lw=2, color='g')
        self.pressure_line, = self.ax4.plot([], [], lw=2, color='b')
        self.stress_line, = self.ax5.plot([], [], lw=2, color='m')

        self.ax1.set_ylabel('Temperature')
        self.ax1.set_xlabel('Time')
        self.ax2.set_ylabel('Production Rate')
        self.ax2.set_xlabel('Time')
        self.ax3.set_ylabel('Power Consumption')
        self.ax3.set_xlabel('Time')
        self.ax4.set_ylabel('Pressure')
        self.ax4.set_xlabel('Time')
        self.ax5.set_ylabel('Stress')
        self.ax5.set_xlabel('Time')

        anim = FuncAnimation(fig, self.update, frames=200, interval=100, blit=False)
        plt.close(fig)
        return HTML(anim.to_jshtml())

machine = ManufacturingMachine(initial_temp=70, max_temp=100, optimal_temp=75, initial_production_rate=10, initial_power=50)
digital_twin = DigitalTwin(machine)
display(digital_twin.visualize())
