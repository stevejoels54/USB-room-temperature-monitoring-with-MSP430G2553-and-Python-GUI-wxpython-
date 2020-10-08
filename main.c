#include <msp430.h> 
/** PROJECT : USB connected room thermometer
 *  MICROCONTROLLER : MSP430G2553
 *  PROGRAMMER : STEVE JOELS
 * main.c
 */
unsigned int ADC_value=0;
void ConfigureAdc(void);
unsigned int Temp;
char realnum[3];
char num[10]={'0','1','2','3','4','5','6','7','8','9'}; // Array with char numbers
void UART_TX(char *tx_data) // Transmit function that only allows char type parameters
{
    unsigned int i=0;
    while(tx_data[i])
    {
        while((UCA0STAT & UCBUSY));
        UCA0TXBUF = tx_data[i];
        i++;
    }
}
void ConfigureAdc(void)
{
    ADC10CTL0 = SREF_0 + ADC10SHT_3 + REFON + ADC10ON;  // Vcc & Vss as reference, Sample and hold for 64 Clock cycles, ADC on, ADC interrupt enable
    ADC10CTL1 = INCH_10 + ADC10DIV_3 ;         // Channel 0, ADC10CLK/3
}
void main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	DCOCTL = 0; // Select lowest DCOx and MODx settings
	BCSCTL1 = CALBC1_1MHZ; // Set DCO
	DCOCTL = CALDCO_1MHZ;

    //P1DIR |= BIT0+BIT6;
	//P1OUT &=~BIT0+BIT6;
	
	P1SEL |= BIT1+BIT2; // UART rx and tx pins
	P1SEL2 |= BIT1+BIT2;

	UCA0CTL1 |= UCSSEL_2+UCSWRST;
	UCA0BR0 = 104; // 9600 baud rate
	UCA0BR1 = 0;
	UCA0MCTL = UCBRS_1;
	UCA0STAT |= UCLISTEN;
	UCA0CTL1 &=~UCSWRST;

	IE2 |= UCA0TXIE;
	IE2 |= UCA0RXIE;
	ConfigureAdc();
	while(1)
	{
	 __delay_cycles(1000);               // Wait for ADC Ref to settle
	 ADC10CTL0 |= ENC + ADC10SC;         // Sampling and conversion start
    ADC_value = ADC10MEM;// Assigns the value held in ADC10MEM to the integer called ADC_value
    Temp=((ADC_value-673)*423)/1024; // convert value between 0 and 1024 to temperature in celcius
    Temp=Temp-20; // make value more accurate depending on calibrated value
    realnum[0]=num[Temp/10]; // get 1st temp value which is int and convert it to char
    realnum[1]=num[Temp%10]; // get 2nd temp value which is int and convert it to char
	UART_TX(realnum); // Transmit temperature values from the array realnum that stores them
	UART_TX("\r\n");
	_delay_cycles(1000000);
     }
	}
