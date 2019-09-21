#define F_CPU 16000000
#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>
#include <ads1292r.h>
#include <SPI.h>

ads1292r ADS1292;   // define class

volatile uint8_t  SPI_Dummy_Buff[30];
uint8_t DataPacketHeader[16];
volatile signed long s32DaqVals[8];
uint8_t data_len = 8;
volatile byte SPI_RX_Buff[15] ;
volatile static int SPI_RX_Buff_Count = 0;
volatile char *SPI_RX_Buff_Ptr;
volatile bool ads1292dataReceived =false;
unsigned long uecgtemp = 0;
signed long secgtemp=0;
int i,j;

byte k = 0;
byte tmpstr[5];
byte zsync = 0;
byte wait = 0;
byte cycle = 0;
char c;

float temp=0.0;

void setup()
{
 //USART1 INIT - SpO2 INIT
 
 UCSR1B = 0x00;
 UCSR1A = 0x00;
 UCSR1C = 0x06;
 UBRR1L = 0x08; 
 UBRR1H = 0x00; 
 UCSR1B = 0x98;

 //USART0 INIT - Data Transmission To PC
 
 Serial.begin(9600);

 //ECG Shield INIT
 
 pinMode(ADS1292_DRDY_PIN, INPUT);  //6
 pinMode(ADS1292_CS_PIN, OUTPUT);    //7
 pinMode(ADS1292_START_PIN, OUTPUT);  //5
 pinMode(ADS1292_PWDN_PIN, OUTPUT);  //4
  
 ADS1292.ads1292_Init();  //initalize ADS1292 slave

 //LM35 INIT
 pinMode(A0, OUTPUT);
 pinMode(A1, INPUT);
 pinMode(A2, OUTPUT);

 digitalWrite(A0, HIGH);
 digitalWrite(A2, LOW);
}

void loop()
{
  if((digitalRead(ADS1292_DRDY_PIN)) == LOW)       // Sampling rate is set to 125SPS ,DRDY ticks for every 8ms
  {                                                  
    SPI_RX_Buff_Ptr = ADS1292.ads1292_Read_Data(); // Read the data,point the data to a pointer

    for(i = 0; i < 9; i++)
    {
      SPI_RX_Buff[SPI_RX_Buff_Count++] = *(SPI_RX_Buff_Ptr + i);  // store the result data in array
    }
    ads1292dataReceived = true;
  }
  
  if(ads1292dataReceived == true)       // process the data 
  {     
    j=0;
    for(i=0;i<6;i+=3)                  // data outputs is (24 status bits + 24 bits Respiration data +  24 bits ECG data) 
    {

        uecgtemp = (unsigned long) (  ((unsigned long)SPI_RX_Buff[i+3] << 16) | ( (unsigned long) SPI_RX_Buff[i+4] << 8) |  (unsigned long) SPI_RX_Buff[i+5]);
        uecgtemp = (unsigned long) (uecgtemp << 8);
        secgtemp = (signed long) (uecgtemp);
        secgtemp = (signed long) (secgtemp >> 8);

        s32DaqVals[j++]=secgtemp;
    }
 
    DataPacketHeader[1] = s32DaqVals[1];            // 4 bytes ECG data
    DataPacketHeader[2] = s32DaqVals[1]>>8;
    DataPacketHeader[3] = s32DaqVals[1]>>16;
    DataPacketHeader[4] = s32DaqVals[1]>>24; 
    
    DataPacketHeader[5] = s32DaqVals[0];            // 4 bytes Respiration data
    DataPacketHeader[6] = s32DaqVals[0]>>8;
    DataPacketHeader[7] = s32DaqVals[0]>>16;
    DataPacketHeader[8] = s32DaqVals[0]>>24; 


    Serial.println("1101");
    for(i=1; i<9; i++) 
    {
      Serial.println(DataPacketHeader[i]);     // transmit the data over USB
     } 
   }
    ads1292dataReceived = false;
    SPI_RX_Buff_Count = 0;

    temp = (5.0 * analogRead(A1) * 100.0) / 1024;
  
}


ISR(USART1_RX_vect)
{
  c = UDR1;
  if((byte)c == 0x00)
  {
    cycle++;  /* wait a few zero synch bytes */
    zsync = 1;
    i = 0;
  }
  if(zsync == 1 && cycle == 10)
  {
    if((byte)c != 0xFF)
    {
      tmpstr[i] = c;
      if(i == 3)
      {
        Serial.println(tmpstr[1]);
        Serial.println(tmpstr[2]);
        Serial.println(tmpstr[3]);
        Serial.println(temp);
        zsync = 0;
        wait = 1;
        cycle = 0;
      }
      i++;
    }
  }
}

