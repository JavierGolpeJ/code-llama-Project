import java.util.NoSuchElementException;


public class ArrayStack<T> {

    public static final int INITIAL_CAPACITY = 9;

    private T[] backingArray;
    private int size;

    public ArrayStack() {
        backingArray = (T[]) new Object[INITIAL_CAPACITY];
        size = 0;
    }

    public void push(T data) {
        if (data == null) {
            throw new IllegalArgumentException();
        }
        if (size == 0) {
            backingArray[0] = data;
            size++;
            return;
        }
        if (size == INITIAL_CAPACITY) {
            expand();
        }
        backingArray[size] = data;
        size++;
    }

    public T pop() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        T thisData = backingArray[size - 1];
        backingArray[size - 1] = null;
        size--;
        return thisData;
    }


    public T peek() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        return backingArray[size - 1];
    }


    public T[] getBackingArray() {
        // DO NOT MODIFY THIS METHOD!
        return backingArray;
    }

    private void expand() {
        T[] largerBackingArray = (T[]) new Object[backingArray.length * 2];
        int currInd = 0;
        while (currInd < backingArray.length) {
            largerBackingArray[currInd] = backingArray[currInd];
            currInd++;
        }
        backingArray = largerBackingArray;
    }


    public int size() {
        // DO NOT MODIFY THIS METHOD!
        return size;
    }
}