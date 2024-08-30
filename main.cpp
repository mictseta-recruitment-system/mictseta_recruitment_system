#include <iostream>

using namespace std;

class Car{
protected:
    string make;
    string model;
    int year;
    int speed= 0;
    bool engine = false;

    void setMake(string m){
    make = m;
    }

    void setModel(string mo){
    model = mo;
    }

    void setYear(int y){
    year = y;
    }

    void getDetails(){
         cout <<" " <<endl;
        cout << "make : "  << make << endl;
        cout << "model : " << model << endl;
        cout << "year : " << year << endl;
         cout <<" " <<endl;
    }

    void startEngine(){
        engine = true;
         cout <<" " <<endl;
        cout << " starting Engine ........"<<endl;
         cout <<" " <<endl;
    }

    void accelerate(){
        if (engine == true ){

            speed = speed +20;
            cout <<" " <<endl;
            cout << "now we moving at " << speed << "km/h"<<endl;
            cout <<" " <<endl;
        }else{
            cout <<" "<< endl;
            cout << "start engine to move car" << endl;
            cout << " " << endl;
        }
    }

    void brake(){

        if (engine == true ){
            speed = speed - 20;
            cout <<" " <<endl;
            cout << "now we moving at " << speed << "km/h"<<endl;
            cout <<" " <<endl;
        }else{
             cout <<" " <<endl;
            cout << "Car is not moving" << endl;
             cout <<" " <<endl;
        }
    }
};


class Benz : protected Car{
public:
    string inputMake;
    string inputModel;
    int inputYear;

    void displayType(){
        cout << "CAR - BENZ" << endl;
        getDetails();
    }
    void start(){
        startEngine();
    }
    void acc(){
        accelerate();
    }
    void brakes(){
        brake();
    }
    void setDetails(){
        setMake(inputMake);
        setModel(inputModel);
        setYear(inputYear);
    }
    void setDetails(string make, string model, int year){
        setMake(make);
        setModel(model);
        setYear(year);
    }

};

class POLO : protected Car{
public:

    void displayType(){
        cout << "CAR - POLO" << endl;
        getDetails();
    }
     void start(){
        startEngine();
    }
    void acc(){
        accelerate();
    }
    void brakes(){
        brake();
    }
     void setDetails(string make, string model, int year){
        setMake(make);
        setModel(model);
        setYear(year);
    }
};



int main()
{

    Benz benz;
    POLO polo;

    while(true){
    int opt;
    cout << "1. start engine" << endl;
    cout << "2. accelerate" << endl;
    cout << "3. brake" << endl;
    cout << "4. change details" << endl;
    cout << "5. get details" << endl;
    cout << "0. Exit" << endl;

    cout <<"choose option : ";
    cin >> opt;
    switch(opt){
        case 1:
            benz.start();
            break;
        case 2 :
            benz.acc();
            break;
        case 3 :
            benz.brakes();
            break;
        case 4:
            cout << "enter make : " ;
            cin >> benz.inputMake;

            cout << "enter model : " ;
            cin >> benz.inputModel;

            cout << "enter years : " ;
            cin >> benz.inputYear;

            benz.setDetails();
           break;
        case 5:
            benz.displayType();
            break;
        case 0 :
            return 0;
    }


    }



    return 0;
}
