class MotorController:
    def __init__(self, use_gpio=False, left_pin=18, right_pin=19):
        self.use_gpio = use_gpio

        if use_gpio:
            try:
                from gpiozero import PWMOutputDevice
                self.left_motor = PWMOutputDevice(left_pin)
                self.right_motor = PWMOutputDevice(right_pin)
            except ImportError:
                print("gpiozero not available. Falling back to simulated motors.")
                self.use_gpio = False

    def set_speeds(self, left, right):
        if self.use_gpio:
            self.left_motor.value = abs(left)
            self.right_motor.value = abs(right)
        else:
            print(f"Motor: L={left:.3f}, R={right:.3f}")

    def stop(self):
        self.set_speeds(0.0, 0.0)
