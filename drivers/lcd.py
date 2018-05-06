# Copyright (C) Waveshare     July 10 2017
# Reorganised / refactored for personal use only.
# Do not redistribute any futrther.

import RPi.GPIO as GPIO
import spidev
import time


# SPI device, bus = 0, device = 0
SPI = spidev.SpiDev(0, 0)

# Pin definition
RST_PIN         = 27
DC_PIN          = 25
CS_PIN          = 8
BL_PIN          = 24

LCD_WIDTH  = 128 #LCD width
LCD_HEIGHT = 128 #LCD height
x = 2
y = 1

x_MAXPIXEL = 132  #LCD width maximum memory
y_MAXPIXEL = 162  #LCD height maximum memory

# scanning method
L2R_U2D = 1
L2R_D2U = 2
R2L_U2D = 3
R2L_D2U = 4
U2D_L2R = 5
U2D_R2L = 6
D2U_L2R = 7
D2U_R2L = 8
SCAN_DIR_DFT = U2D_R2L

##***********************************************************************************************************************
#------------------------------------------------------------------------
#|\\\																#/|
#|\\\						Drive layer								#/|
#|\\\																#/|
#------------------------------------------------------------------------
#************************************************************************************************************************
class LCD:
    def __init__(self):
        self.dis_column = LCD_WIDTH
        self.dis_page = LCD_HEIGHT
        self.scan_dir = SCAN_DIR_DFT
        self.x_adjust = x
        self.y_adjust = y

    """    Hardware reset     """
    def  reset(self):
        GPIO.output(RST_PIN, GPIO.HIGH)
        self.driver_delay_ms(100)
        GPIO.output(RST_PIN, GPIO.LOW)
        self.driver_delay_ms(100)
        GPIO.output(RST_PIN, GPIO.HIGH)
        self.driver_delay_ms(100)

    """    Write register address and data     """
    def  writeReg(self, Reg):
        GPIO.output(DC_PIN, GPIO.LOW)
        self.SPI_Write_Byte([Reg])

    def writeData_8bit(self, Data):
        GPIO.output(DC_PIN, GPIO.HIGH)
        self.SPI_Write_Byte([Data])

    def writeData_NLen16Bit(self, Data, DataLen):
        GPIO.output(DC_PIN, GPIO.HIGH)
        for i in range(0, DataLen):
            self.SPI_Write_Byte([Data >> 8])
            self.SPI_Write_Byte([Data & 0xff])

    """    Common register initialization    """
    def initReg(self):
        #ST7735R Frame Rate
        self.writeReg(0xB1)
        self.writeData_8bit(0x01)
        self.writeData_8bit(0x2C)
        self.writeData_8bit(0x2D)

        self.writeReg(0xB2)
        self.writeData_8bit(0x01)
        self.writeData_8bit(0x2C)
        self.writeData_8bit(0x2D)

        self.writeReg(0xB3)
        self.writeData_8bit(0x01)
        self.writeData_8bit(0x2C)
        self.writeData_8bit(0x2D)
        self.writeData_8bit(0x01)
        self.writeData_8bit(0x2C)
        self.writeData_8bit(0x2D)

        #Column inversion
        self.writeReg(0xB4)
        self.writeData_8bit(0x07)

        #ST7735R Power Sequence
        self.writeReg(0xC0)
        self.writeData_8bit(0xA2)
        self.writeData_8bit(0x02)
        self.writeData_8bit(0x84)
        self.writeReg(0xC1)
        self.writeData_8bit(0xC5)

        self.writeReg(0xC2)
        self.writeData_8bit(0x0A)
        self.writeData_8bit(0x00)

        self.writeReg(0xC3)
        self.writeData_8bit(0x8A)
        self.writeData_8bit(0x2A)
        self.writeReg(0xC4)
        self.writeData_8bit(0x8A)
        self.writeData_8bit(0xEE)

        self.writeReg(0xC5)#VCOM
        self.writeData_8bit(0x0E)

        #ST7735R Gamma Sequence
        self.writeReg(0xe0)
        self.writeData_8bit(0x0f)
        self.writeData_8bit(0x1a)
        self.writeData_8bit(0x0f)
        self.writeData_8bit(0x18)
        self.writeData_8bit(0x2f)
        self.writeData_8bit(0x28)
        self.writeData_8bit(0x20)
        self.writeData_8bit(0x22)
        self.writeData_8bit(0x1f)
        self.writeData_8bit(0x1b)
        self.writeData_8bit(0x23)
        self.writeData_8bit(0x37)
        self.writeData_8bit(0x00)
        self.writeData_8bit(0x07)
        self.writeData_8bit(0x02)
        self.writeData_8bit(0x10)

        self.writeReg(0xe1)
        self.writeData_8bit(0x0f)
        self.writeData_8bit(0x1b)
        self.writeData_8bit(0x0f)
        self.writeData_8bit(0x17)
        self.writeData_8bit(0x33)
        self.writeData_8bit(0x2c)
        self.writeData_8bit(0x29)
        self.writeData_8bit(0x2e)
        self.writeData_8bit(0x30)
        self.writeData_8bit(0x30)
        self.writeData_8bit(0x39)
        self.writeData_8bit(0x3f)
        self.writeData_8bit(0x00)
        self.writeData_8bit(0x07)
        self.writeData_8bit(0x03)
        self.writeData_8bit(0x10)

        #Enable test command
        self.writeReg(0xF0)
        self.writeData_8bit(0x01)

        #Disable ram power save mode
        self.writeReg(0xF6)
        self.writeData_8bit(0x00)

        #65k mode
        self.writeReg(0x3A)
        self.writeData_8bit(0x05)

    #********************************************************************************
    #function:	Set the display scan and color transfer modes
    #parameter: 
    #		Scan_dir   :   Scan direction
    #		Colorchose :   RGB or GBR color format
    #********************************************************************************
    def setGramScanWay(self, scan_dir):
        #Get the screen scan direction
        self.scan_dir = scan_dir

        #Get GRAM and LCD width and height
        if (scan_dir == L2R_U2D) or (scan_dir == L2R_D2U) or (scan_dir == R2L_U2D) or (scan_dir == R2L_D2U) :
            self.dis_column	= LCD_HEIGHT 
            self.dis_page 	= LCD_WIDTH 
            if scan_dir == L2R_U2D:
                MemoryAccessReg_Data = 0X00 | 0x00
            elif scan_dir == L2R_D2U:
                MemoryAccessReg_Data = 0X00 | 0x80
            elif scan_dir == R2L_U2D:
                MemoryAccessReg_Data = 0x40 | 0x00
            else:		#R2L_D2U:
                MemoryAccessReg_Data = 0x40 | 0x80
        else:
            self.dis_column	= LCD_WIDTH 
            self.dis_page 	= LCD_HEIGHT 
            if scan_dir == U2D_L2R:
                MemoryAccessReg_Data = 0X00 | 0x00 | 0x20
            elif scan_dir == U2D_R2L:
                MemoryAccessReg_Data = 0X00 | 0x40 | 0x20
            elif scan_dir == D2U_L2R:
                MemoryAccessReg_Data = 0x80 | 0x00 | 0x20
            else:		#R2L_D2U
                MemoryAccessReg_Data = 0x40 | 0x80 | 0x20

        #please set (MemoryAccessReg_Data & 0x10) != 1
        if (MemoryAccessReg_Data & 0x10) != 1:
            self.x_adjust = y
            self.y_adjust = x
        else:
            self.x_adjust = x
            self.y_adjust = y

        # Set the read / write scan direction of the frame memory
        self.writeReg(0x36)		#MX, MY, RGB mode 
        self.writeData_8bit( MemoryAccessReg_Data | 0x08)	#0x08 set RGB


    def turnOn(self):
        self.isOn = True
        if (self.GPIO_Init() == 0):
            GPIO.output(BL_PIN,GPIO.HIGH)


    def turnOff(self):
        self.isOn = False
        if (self.GPIO_Init() == 0):
            GPIO.output(BL_PIN,GPIO.LOW)

    def isTurnedOn(self):
        return self.isOn


    #/********************************************************************************
    #function:	
    #			initialization
    #********************************************************************************/
    def init(self, Lcd_ScanDir=SCAN_DIR_DFT):
        if (self.GPIO_Init() != 0):
            return -1

        #Turn on the backlight
        self.isOn = True
        GPIO.output(BL_PIN,GPIO.HIGH)

        #Hardware reset
        self.reset()

        #Set the initialization register
        self.initReg()

        #Set the display scan and color transfer modes	
        self.setGramScanWay( Lcd_ScanDir )
        self.driver_delay_ms(200)

        #sleep out
        self.writeReg(0x11)
        self.driver_delay_ms(120)

        #Turn on the LCD display
        self.writeReg(0x29)

        # self.clear()

    #/********************************************************************************
    #function:	Sets the start position and size of the display area
    #parameter: 
    #	Xstart 	:   X direction Start coordinates
    #	Ystart  :   Y direction Start coordinates
    #	Xend    :   X direction end coordinates
    #	Yend    :   Y direction end coordinates
    #********************************************************************************/
    def setWindows(self, Xstart, Ystart, Xend, Yend ):
        #set the X coordinates
        self.writeReg ( 0x2A )
        self.writeData_8bit ( 0x00 )                                 #Set the horizontal starting point to the high octet
        self.writeData_8bit ( (Xstart & 0xff) + self.x_adjust)       #Set the horizontal starting point to the low octet
        self.writeData_8bit ( 0x00 )                                 #Set the horizontal end to the high octet
        self.writeData_8bit ( (( Xend - 1 ) & 0xff) + self.x_adjust) #Set the horizontal end to the low octet

        #set the Y coordinates
        self.writeReg ( 0x2B )
        self.writeData_8bit ( 0x00 )
        self.writeData_8bit ( (Ystart & 0xff) + self.y_adjust)
        self.writeData_8bit ( 0x00 )
        self.writeData_8bit ( ( (Yend - 1) & 0xff )+ self.y_adjust)

        self.writeReg(0x2C)

    #/********************************************************************************
    #function:	Set the display point (Xpoint, Ypoint)
    #parameter: 
    #		xStart :   X direction Start coordinates
    #		xEnd   :   X direction end coordinates
    #********************************************************************************/
    def setCursor (self, Xpoint, Ypoint ):
        self.setWindows ( Xpoint, Ypoint, Xpoint , Ypoint )

    #/********************************************************************************
    #function:	Set show color
    #parameter: 
    #		Color  :   Set show color
    #********************************************************************************/
    def setColor(self, Color , width,  height):
        self.writeData_NLen16Bit(Color,width * height)

    #/********************************************************************************
    #function:	Point (Xpoint, Ypoint) Fill the color
    #parameter: 
    #		Xpoint :   The x coordinate of the point
    #		Ypoint :   The y coordinate of the point
    #		Color  :   Set the color
    #********************************************************************************/
    def setPointlColor (self,  Xpoint,  Ypoint, Color ):
        if ( ( Xpoint <= self.dis_column ) and ( Ypoint <= self.dis_page ) ):
            self.setCursor (Xpoint, Ypoint)
            self.setColor ( Color , 1 , 1)

    #/********************************************************************************
    #function:	Fill the area with the color
    #parameter: 
    #		Xstart :   Start point x coordinate
    #		Ystart :   Start point y coordinate
    #		Xend   :   End point coordinates
    #		Yend   :   End point coordinates
    #		Color  :   Set the color
    #********************************************************************************/
    def setArealColor (self, Xstart, Ystart, Xend, Yend, Color):
        if (Xend > Xstart) and (Yend > Ystart):
            self.setWindows( Xstart , Ystart , Xend , Yend  )
            self.setColor ( Color ,Xend - Xstart , Yend - Ystart )

    #/********************************************************************************
    #function:	
    #			Clear screen 
    #********************************************************************************/
    def clear(self):
        self.setArealColor(0,0, x_MAXPIXEL , y_MAXPIXEL, Color = 0xFFFF)#white

    def showImage(self, image):
        if (image == None):
            return

        self.setWindows(0, 0, self.dis_column , self.dis_page)
        pixels = image.load()
        for j in range(0, self.dis_page ):
            for i in range(0, self.dis_column ):
                pixels_Color = ((pixels[i, j][0] >> 3) << 11)|((pixels[i, j][1] >> 2) << 5)|(pixels[i, j][2] >> 3)#RGB Data
                self.setColor(pixels_Color , 1, 1)



    def drawRect(self, image, x, y, w, h):
        self.setWindows(x,y,w,h)
        pixels = image.load()
        for j in range(0, h):
            for i in range(0, w):
                px = pixels[i, j]
                pixels_color = ((px[0] >> 3) << 11)|((px[1] >> 2) << 5)|(px[2] >> 3)#RGB Data
                self.setColor(pixels_color, 1, 1)

    def driver_delay_ms(self, xms):
        time.sleep(xms / 1000.0)

    def SPI_Write_Byte(self, data):
        SPI.writebytes(data)

    def GPIO_Init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.setup(DC_PIN, GPIO.OUT)
        GPIO.setup(CS_PIN, GPIO.OUT)
        GPIO.setup(BL_PIN, GPIO.OUT)
        SPI.max_speed_hz = 9000000
        SPI.mode = 0b00
        return 0;

    def GPIO_Cleanup(self):
        GPIO.cleanup()


if __name__ == '__main__':
    import Image
    import ImageDraw
    import ImageFont
    import ImageColor

    LCD = LCD()

    print("**********Init LCD**********")
    LCD.init(SCAN_DIR_DFT) #SCAN_DIR_DFT = D2U_L2R

    image = Image.new("RGB", (LCD.dis_column, LCD.dis_page), "WHITE")
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
    print("***draw line")
    draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
    draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
    draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
    draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
    print("***draw rectangle")
    draw.rectangle([(18,10),(110,20)],fill = "RED")

    print("***draw text")
    draw.text((33, 22), 'WaveShare ', fill = "BLUE")
    draw.text((32, 36), 'Electronic ', fill = "BLUE")
    draw.text((28, 48), '1.44inch LCD ', fill = "BLUE")

    LCD.showImage(image,0,0)
    LCD.driver_delay_ms(500)

    # image = Image.open('time.bmp')
    # LCD.showImage(image,0,0)

    LCD.GPIO_Cleanup()

