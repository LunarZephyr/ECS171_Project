#include "LongInt.h"
#include "StackLi.h"

using namespace std;

LongInt::LongInt()
{
    StackLi<int> stack;
    int count;
}

LongInt& operator+(LongInt& a, LongInt& b){
    StackLi<int> tempstack;
    int diff = a.count - b.count;
    int av;
    int bv;
    int add;
    int left = 0;
    while(!a.stack.isEmpty() && !b.stack.isEmpty())
    {
        av = a.stack.topAndPop();
        bv = b.stack.topAndPop();
        add = av + bv + left;
        left = 0;
        if (!a.stack.isEmpty() || !b.stack.isEmpty())
        {
            if (add > 9) {
                add -= 10;
                left = 1;
            }
        }
        tempstack.push(add);
    }
    if (diff >= 0) 
    {
        if (diff > 0) {tempstack.push(a.stack.topAndPop() + left);}
        while(!tempstack.isEmpty()) {
            a.stack.push(tempstack.topAndPop());
        }
        return a;
    }
    else if (diff < 0)
    {
        tempstack.push(b.stack.topAndPop() + left);
        while(!tempstack.isEmpty()) {
            b.stack.push(tempstack.topAndPop());
        }
        return b;
    }
    return a;
}

istream& operator>>(istream& input, LongInt& L)
{
    StackLi<int> tempstack;
    char c;
    int i;
    L.count = 0;
    while (input.get(c))
    {
        i = c - 48;
        if (i == -38) {
            break;
        }
        L.stack.push(i);
        L.count += 1;
    }
    return input;
}

ostream& operator<<(ostream& output, LongInt& L)
{
    StackLi<int> newstack;
    while(!L.stack.isEmpty())
    {
        newstack.push(L.stack.topAndPop());
    }
    while(!newstack.isEmpty())
    {
        output << newstack.topAndPop();
    }
    return output;
}