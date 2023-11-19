#include <Arduino.h>
#include <HardwareSerial.h>
#include <sstream>
#include <string>
#include <cstring>
#include <bits/stdc++.h>
#include <iostream>
#include <vector>
using namespace std;
using std::cout;
using std::endl;
// HardwareSerial SerialPort2(2); // use UART0
// HardwareSerial SerialPort2(0); // use UART0
float pH_1 = 0.0;
float pH_2 = 4.0;
float pH_3 = 7.0;
float pH_4 = 14.0;
int randomVal;
String my_string =" ";
String FloatToString  (float a); 
String delimiter;
String sub_string_data;
vector<float> input_data;
vector<float> array_input_data;
//float input_array[0];

class SimpleMovingAverage {
  // queue used to store list so we can get the average
  queue<double> Dataset;
  int period;
  double sum;

  public:
  // constructor to initialize period
  SimpleMovingAverage(int per) { period = per; }

  // function to add new dara in the
  // list & update the sum so that
  // we get the new mean
  void addData (double num)
  {
    sum += num;
    Dataset.push(num);

    // Updating size so that length
    // of data set should be equal
    // to period as a normal mean has
    if (Dataset.size() > period) {
      sum -= Dataset.front();
      Dataset.pop();
    }
  }
  // function to calculate mean
  double getMean() { return sum / period; }
};
   
void displayArr( vector<float> v) {
  for( int i =0; i < v.size(); i++){
    cout << v[ i ] << ", ";
  }
  cout << endl;
}

vector<float> insertAtEnd( vector<float> A, int e ){
   A.push_back( e );
   return A;
}

String find_str(string s, string del) {
    // Use find function to find 1st position of delimiter.
    int end = s.find(del); 
    while (end != -1) { // Loop until no delimiter is left in the string.
        cout << s.substr(0, end) << endl;
        s.erase(s.begin(), s.begin() + end + 1);
        end = s.find(del);
    }
    cout << s.substr(0, end);
    String sub_string = s.substr(0, end);
return sub_string;
}

void setup() {
  Serial.begin(9600);
  //SerialPort2.begin(9600, SERIAL_8N1, 16, 17);
  //Serial2.begin(9600,SERIAL_8N1);
  //Serial.begin(9600, SERIAL_8N1, 16, 17);
}

void loop() {
  /**
  Sample test:
  SerialPort.print(1);
  delay(5000);
  SerialPort.print(0);
  delay(5000); 
  **/

  //my_string = "'" + FloatToString (pH_1) + "','" + FloatToString (pH_2) + "','" + FloatToString (pH_3) + "','" + FloatToString (pH_4)+ "'";

  randomVal = random(0,3);
  my_string = FloatToString (pH_1+randomVal) + "," + FloatToString (pH_2+randomVal) + "," + FloatToString (pH_3+randomVal) + "," + FloatToString (pH_4+randomVal);
  
  Serial.println(my_string);
  /**
  delimiter = ',';
  //string sub_string_data = my_string.c_str(0, my_string.end(delimiter)); 
  sub_string_data = find_str(my_string, delimiter);
  **/


  /**
  //convert string to float
  float float_input_data = std::stof (sub_string_data);
  input_data.push_back(float_input_data);
  **/

  //insertAtEnd(input_data);
  // array of input_data Ex: {0.000, 4.000, 7.000, 10.000}
  /*for (int i=0; i<input_array.size(); i++) {
    input_array[size] = input_data;
  }
  */
  int per = 3;
  SimpleMovingAverage obj(per);
  for (float x : input_data) {
    obj.addData(x);
    cout << "New number added is " << x
      << ", SMA = " << obj.getMean() << endl;
  }
  delay(100);
  
}

String FloatToString  (float a)
{
  String temp = String(a, 3);
        /**
        temp<<a;
        String a;
        **/
  return temp;
}

/*
int main() 
{
  // array of input_data Ex: {0.000, 4.000, 7.000, 10.000}
  float input_data[] = float_input_data;
  int per = 3;
  SimpleMovingAverage obj(per);
  for (float x : input_data) {
    obj.addData(x);
    cout << "New number added is " << x
      << ", SMA = " << obj.getMean() << endl;
  }
}
*/