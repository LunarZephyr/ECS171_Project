#ifndef _LongInt_H
#define _LongInt_H

#include "StackLi.h"

#define LongInt longint

class LongInt; //Incomplete declaration

class LongInt {
    //private:
    public:
        StackLi<int> stack;
        int count;
        LongInt();
        friend LongInt& operator+(LongInt& a, LongInt& b);
        friend istream& operator>>(istream& input, LongInt& L);
        friend ostream& operator<<(ostream& output, LongInt& L);
};

#include "LongInt.cpp"
#endif