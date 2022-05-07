#include <iostream>
#include "LinkedList.h"
#include "CursorList.h"
vector<CursorNode <int> > cursorSpace(500001);
#include "StackAr.h"
#include "StackLi.h"
#include "QueueAr.h"
#include "SkipList.h"
#include "CPUTimer.h"
#include <fstream>

using namespace std;

int getChoice() {
    int x;
    cout << "\tADT Menu\n0. Quit\n1. LinkedList \n2. CursorList \n3. StackAr\n";
    cout << "4. StackLi\n5. QueueAr\n6. SkipList\n";
    cout << "Your choice: ";
    cin >> x;
    return x;
}

void RunList(char* filename) {
    List<int> list;
    ifstream file(filename);
    file.ignore(10000, '\n');
    int integer;
    char letters;
    ListItr<int> pointer = list.zeroth();
    while(file >> letters >> integer)
    {
        if (letters == 'i') {list.insert(integer, pointer);}
        else if (letters == 'd') {list.remove(integer);}
    }
}

void RunCursorList(char* filename) {
    ifstream file(filename);
    file.ignore(10000, '\n');
    int integer;
    char letters;
    CursorList<int> clist(cursorSpace);
    CursorListItr<int> pointer = clist.zeroth();
    while(file >> letters >> integer)
    {  
        if (letters == 'i') {
            clist.insert(integer, pointer);
        }
        else if (letters == 'd') {clist.remove(integer);}
    }
}


void RunStackAr(char* filename) {
    StackAr<int> stack(500001);
    ifstream file(filename);
    file.ignore(10000, '\n');
    int integer;
    char letters;
    while(file >> letters >> integer)
    {
        if (letters == 'i') {stack.push(integer);}
        else if (letters == 'd') {
            stack.pop();
        }
    }
}

void RunStackLi(char* filename) {
    ifstream file(filename);
    file.ignore(10000, '\n');
    int integer;
    char letters;
    StackLi<int> stack;
    while(file >> letters >> integer)
    {
        if (letters == 'i') {stack.push(integer);}
        else if (letters == 'd') {
            stack.pop();
        }
    }
}

void RunQueueAr(char* filename) {
    Queue<int> queue(500001);
    ifstream file(filename);
    file.ignore(10000, '\n');
    int integer;
    char letters;
    while(file >> letters >> integer)
    {
        queue.enqueue(integer);
        if (letters == 'd') {
            queue.dequeue();
        }
    }
}

void RunSkipList(char* filename) {
    SkipList<int> skiplist(0, 500001);
    fstream file(filename);
    file.ignore(10000, '\n');
    int integer;
    char letters;
    while(file >> letters >> integer)
    {
        if(letters == 'i') { skiplist.insert(integer);}
        else if (letters == 'd') {
            skiplist.deleteNode(integer);
        }
    }
}


int main() {
    int choice = 1;
    CPUTimer ct;
    char filename[99];
    cout << "Filename: ";
    cin >> filename;
    do
    {
        choice = getChoice();
        ct.reset();
        switch (choice)
        {
            case 1: RunList(filename); break;
            case 2: RunCursorList(filename); break;
            case 3: RunStackAr(filename); break;
            case 4: RunStackLi(filename); break;
            case 5: RunQueueAr(filename); break;
            case 6: RunSkipList(filename); break;
        }

        cout << "CPU time: " << ct.cur_CPUTime() << endl;
    } while(choice > 0);
    return 0;
}
