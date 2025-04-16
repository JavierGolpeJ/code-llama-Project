import java.util.NoSuchElementException;

/**
 * Your implementation of an ArrayQueue.
 *
 * @author Kiavosh Peynabard
 * @version 1.0
 * @userid YOUR USER ID HERE (i.e. kpeynabard3)
 * @GTID YOUR GT ID HERE (i.e. 903353136)
 *
 * Collaborators: LIST ALL COLLABORATORS YOU WORKED WITH HERE
 *
 * Resources: LIST ALL NON-COURSE RESOURCES YOU CONSULTED HERE
 */
public class ArrayQueue<T> {

    /*
     * The initial capacity of the ArrayQueue.
     *
     * DO NOT MODIFY THIS VARIABLE.
     */
    public static final int INITIAL_CAPACITY = 9;

    /*
     * Do not add new instance variables or modify existing ones.
     */
    private T[] backingArray;
    private int front;
    private int size;

    /**
     * Constructs a new ArrayQueue.
     */
    public ArrayQueue() {
        backingArray = (T[]) new Object[INITIAL_CAPACITY];
        front = 0;
        size = 0;
    }

    /**
     * Adds the data to the back of the queue.
     *
     * If sufficient space is not available in the backing array, resize it to
     * double the current length. When resizing, copy elements to the
     * beginning of the new array and reset front to 0.
     *
     * Must be amortized O(1).
     *
     * @param data the data to add to the back of the queue
     * @throws java.lang.IllegalArgumentException if data is null
     */
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

    /**
     * Removes and returns the data from the front of the queue.
     *
     * Do not shrink the backing array.
     *
     * Replace any spots that you dequeue from with null.
     *
     * If the queue becomes empty as a result of this call, do not reset
     * front to 0.
     *
     * Must be O(1).
     *
     * @return the data formerly located at the front of the queue
     * @throws java.util.NoSuchElementException if the queue is empty
     */
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

    /**
     * Returns the data from the front of the queue without removing it.
     *
     * Must be O(1).
     *
     * @return the data located at the front of the queue
     * @throws java.util.NoSuchElementException if the queue is empty
     */
    public T peek() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        return backingArray[front];
    }

    /**
     * Returns the backing array of the queue.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the backing array of the queue
     */
    public T[] getBackingArray() {
        // DO NOT MODIFY THIS METHOD!
        return backingArray;
    }

    /**
     * Helper method which expands the backing array
     *
     * Array will be expanded by adding INITIAL_CAPACITY to its current length.
     *
     */
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

    /**
     * Returns the size of the queue.
     *
     * For grading purposes only. You shouldn't need to use this method since
     * you have direct access to the variable.
     *
     * @return the size of the queue
     */
    public int size() {
        // DO NOT MODIFY THIS METHOD!
        return size;
    }
    public int getFront() {
        // DO NOT MODIFY THIS METHOD!
        return front;
    }
}