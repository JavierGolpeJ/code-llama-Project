import java.util.NoSuchElementException;

public class ArrayQueue<T> {

    public static final int INITIAL_CAPACITY = 9;


    private T[] backingArray;
    private int front;
    private int size;


    public ArrayQueue() {
        backingArray = (T[]) new Object[INITIAL_CAPACITY];
        front = 0;
        size = 0;
    }


    public void enqueue(T data) {
        if (data == null) {
            throw new IllegalArgumentException();
        }
       if (size == INITIAL_CAPACITY) {
            expand();
            backingArray[front + size] = data;
            size++;
            return;
        }
       if (size < INITIAL_CAPACITY && backingArray[INITIAL_CAPACITY - 1] != null) {
            int backingIndx = -(INITIAL_CAPACITY - (front + size));
            backingArray[backingIndx] = data;
            size++;
            return;
        } else {
            backingArray[front + size] = data;
            size++;
            return;
        }
    }


    public T dequeue() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        T thisData = backingArray[front];
        backingArray[front] = null;
        if (front == backingArray.length - 1) {
            System.out.println(backingArray.length);
            System.out.println(front);
            front = front % (backingArray.length - 1);
        } else {
            front++;
        }
        size--;
        return thisData;
    }


    public T peek() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        return backingArray[front];
    }


    public T[] getBackingArray() {
        // DO NOT MODIFY THIS METHOD!
        return backingArray;
    }


    private void expand() {
        T[] largerBackingArray = (T[]) new Object[backingArray.length * 2];
        int counter = 0;
        int newArrIndx = 0;
        int currInd = front;
        while (counter < backingArray.length) {
            if (currInd == backingArray.length) {
                currInd = 0;
            }
            largerBackingArray[newArrIndx] = backingArray[currInd];
            counter++;
            newArrIndx++;
            currInd++;
        }
        backingArray = largerBackingArray;
        front = 0;
    }

    public int size() {
        // DO NOT MODIFY THIS METHOD!
        return size;
    }
    public int getFront() {
        // DO NOT MODIFY THIS METHOD!
        return front;
    }
}