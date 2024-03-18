import wpilib
import wpilib.drive
from cscore import CameraServer


# Ehawks6199
class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # ------------- Motores Tracción ------------- #
        self.left_motor = wpilib.PWMVictorSPX(8)
        self.right_motor = wpilib.PWMVictorSPX(9)

        # ------------- Motores Botones ------------- #
        self.recolector = wpilib.PWMSparkMax(7)
        self.lanzador = wpilib.PWMSparkMax(6)
        self.recoleccion = wpilib.VictorSP(0)
        self.escalada = wpilib.VictorSP(5)

        # ------------- Controladores ------------- #
        # - Se crea un objeto de tipo DifferentialDrive que recibe como parámetros los motores de
        #   tracción izquierdo y derecho para poder controlarlos
        self.drive = wpilib.drive.DifferentialDrive(self.left_motor, self.right_motor)
        # - Se crea un objeto de tipo Joystick que recibe como parámetro el puerto al que está conectado
        self.stick = wpilib.Joystick(1)
        # - Se crea un objeto de tipo Timer para poder controlar el tiempo
        self.timer = wpilib.Timer()

        # ------------- Cámara Configuration ------------- #
        # - Se crea un objeto de tipo CameraServer para poder transmitir la señal de la cámara
        cs = CameraServer()
        # - Se inicia la cámara automática con una resolución de 640x480
        self.camera = cs.startAutomaticCapture()
        self.camera.setResolution(640, 480)

    def autonomousInit(self):
        # - Esta función se ejecuta una vez cada vez que el robot entra en modo autónomo - #
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        # - Esta función se llama periódicamente durante el funcionamiento autónomo - #

        # - Si el temporizador es menor a 2 segundos, el robot avanza a la mitad de su velocidad
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-0.5, 0)  # - El robot avanza a la mitad de su velocidad
        else:
            self.drive.arcadeDrive(0, 0)  # - El robot se detiene

    def teleopPeriodic(self):
        # - Esta función se llama periódicamente durante el teleoperado - #
        lanzadorVelocidad = 1.0

        self.drive.arcadeDrive(self.stick.getX(), self.stick.getY())

        # --------- RECOLECTOR --------- #
        if self.stick.getRawButton(1):
            self.recolector.set(lanzadorVelocidad)
        else:
            self.recolector.set(0.0)

        # --------- LANZADOR --------- #
        if self.stick.getRawButton(2):
            self.lanzador.set(1)
        else:
            self.lanzador.set(0.0)

        # --------- ESCALADA --------- #
        if self.stick.getRawButton(3):
            self.escalada.set(-1)
        elif self.stick.getRawButton(5):
            self.escalada.set(1.0)
        else:
            self.escalada.set(0)

        # --------- RECOLECCION --------- #
        if self.stick.getRawButton(4):
            self.recoleccion.set(1)
        else:
            self.recoleccion.set(0.0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
