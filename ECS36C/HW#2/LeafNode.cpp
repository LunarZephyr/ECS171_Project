#include <iostream>
#include <climits>
#include "LeafNode.h"
#include "InternalNode.h"
#include "QueueAr.h"

using namespace std;


LeafNode::LeafNode(int LSize, InternalNode *p,
  BTreeNode *left, BTreeNode *right) : BTreeNode(LSize, p, left, right)
{
  values = new int[LSize];
}  // LeafNode()

void LeafNode::addToLeft(int value, int last)
{
  leftSibling->insert(values[0]);

  for(int i = 0; i < count - 1; i++)
    values[i] = values[i + 1];

  values[count - 1] = last;
  if(parent)
    parent->resetMinimum(this);
} // LeafNode::ToLeft()

void LeafNode::addToRight(int value, int last)
{
  rightSibling->insert(last);

  if(value == values[0] && parent)
    parent->resetMinimum(this);
} // LeafNode::addToRight()

void LeafNode::addToThis(int value)
{
  int i;

  for(i = count - 1; i >= 0 && values[i] > value; i--)
      values[i + 1] = values[i];

  values[i + 1] = value;
  count++;

  if(value == values[0] && parent)
    parent->resetMinimum(this);
} // LeafNode::addToThis()


void LeafNode::addValue(int value, int &last)
{
  int i;

  if(value > values[count - 1])
    last = value;
  else
  {
    last = values[count - 1];

    for(i = count - 2; i >= 0 && values[i] > value; i--)
      values[i + 1] = values[i];
    // i may end up at -1
    values[i + 1] = value;
  }
} // LeafNode:: addValue()


int LeafNode::getMaximum()const
{
  if(count > 0)  // should always be the case
    return values[count - 1];
  else
    return INT_MAX;
} // getMaximum()


int LeafNode::getMinimum()const
{
  if(count > 0)  // should always be the case
    return values[0];
  else
    return 0;

} // LeafNode::getMinimum()


LeafNode* LeafNode::insert(int value)
{
  int last;

  if(count < leafSize)
  {
    addToThis(value);
    return NULL;
  } // if room for value

  addValue(value, last);

  if(leftSibling && leftSibling->getCount() < leafSize)
  {
    addToLeft(value, last);
    return NULL;
  }
  else // left sibling full or non-existent
    if(rightSibling && rightSibling->getCount() < leafSize)
    {
      addToRight(value, last);
      return NULL;
    }
    else // both siblings full or non-existent
      return split(value, last);
}  // LeafNode::insert()

void LeafNode::print(Queue <BTreeNode*> &queue)
{
  cout << "Leaf: ";
  for (int i = 0; i < count; i++)
    cout << values[i] << ' ';
  cout << endl;
} // LeafNode::print()


LeafNode* LeafNode::remove(int value)
{   // To be written by students
  int check;
  int leafLimit;
  if(leafSize%2 != 0)
    leafLimit = (leafSize/2)+1;
  else
    leafLimit = leafSize/2;
  int index;
  for (int i = 0; i < count; i++)
  {
    if(values[i] == value)
    {
      index = i;
      values[i] = NULL;
    } 
  }

 //reindexing leaf
  for(int k = index; k<count;k++)
    values[k] = values[k+1];

  --count;

 //conditional for merge or borrow left or right
  if(this->getCount() < leafLimit)
  {
    check = borrow();
  }

  if(parent)
    parent->resetMinimum(this);

  if (check == 0)
    return NULL;  // filler for stub
  else
    return this;

}  // LeafNode::remove()


int LeafNode::borrow()
{
  int borrowed;
  int leafLimit;
  if(leafSize%2 != 0)
    leafLimit = (leafSize/2)+1;
  else
    leafLimit = leafSize/2;


  if(leftSibling && leftSibling->getCount() > leafLimit)
  {
    borrowed = leftSibling->getMaximum();
    addToThis(borrowed);
    leftSibling->remove(borrowed);
    if(parent)
      parent->resetMinimum(this);
    return (0);
  }
  else if(leftSibling && leftSibling->getCount() <= leafLimit)
  {
    merge(0);
    if(parent)
      parent->resetMinimum(this);
    return (1);
  }
  else if(rightSibling && rightSibling->getCount() > leafLimit)
  {

    borrowed = rightSibling->getMinimum();
    addToThis(borrowed);
    rightSibling->remove(borrowed);
    if(parent)
      parent->resetMinimum(this);
    return(0);
  }
  else if(rightSibling && rightSibling->getCount() <= leafLimit)
  {
    merge(1);
    if (parent)
      parent->resetMinimum(this);
    return(1);
  }
}

void LeafNode::merge(int x)
{
  int index;
  int value;
  if(x==0)//merge left
  {
    for(int i = 0; i < count; i++ )
    {
      this->addToLeft(this->getMaximum(), this->getMaximum());
      value = this->getMinimum();
      for (int i = 0; i < count; i++)
      {
        if(values[i] == value)
        {
          index = i;
          values[i] = NULL;
        } 
      }
      for(int k = index; k<count;k++)
        values[k] = values[k+1];

      --count;
      if(parent)
        parent->resetMinimum(this);
    }
    if(leftSibling)
      leftSibling->setRightSibling(rightSibling);
  }
  else if(x==1)//merge right
  {
    while(count > 0)
    {
      addToRight(this->getMinimum(), this->getMaximum());
      value = this->getMaximum();
      for (int i = 0; i < count; i++)
      {
        if(values[i] == value)
          values[i] = NULL;
      }

      --count;
      if(parent)
        parent->resetMinimum(this);
    }
    if(leftSibling)
      rightSibling->setLeftSibling(leftSibling);
  }

}

LeafNode* LeafNode::split(int value, int last)
{
  LeafNode *ptr = new LeafNode(leafSize, parent, this, rightSibling);


  if(rightSibling)
    rightSibling->setLeftSibling(ptr);

  rightSibling = ptr;

  for(int i = (leafSize + 1) / 2; i < leafSize; i++)
    ptr->values[ptr->count++] = values[i];

  ptr->values[ptr->count++] = last;
  count = (leafSize + 1) / 2;

  if(value == values[0] && parent)
    parent->resetMinimum(this);
  return ptr;
} // LeafNode::split()
