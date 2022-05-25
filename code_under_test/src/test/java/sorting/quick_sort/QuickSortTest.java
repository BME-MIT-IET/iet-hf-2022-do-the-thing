package sorting.quick_sort;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static sorting.ArraySorter.*;

class QuickSortTest {

    private static QuickSort qcs = new QuickSort();
    private int[] array;
    private static final int[] values = {100,1000,10000};
    private static ArrayList<Long> performance = new ArrayList<>();

    @BeforeAll
    public static void introduction() {
        System.out.println(qcs.getClass().getName());
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void quickSort_inc(int length) {
        System.out.println("Sorted array, " + length + " element");
        int[] sol = inc(new int[length]);
        array = inc(new int[length]);

        long startTime = System.nanoTime();
        qcs.sort(array,0, array.length-1);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        assertArrayEquals(array,sol);
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void quickSort_desc(int length) {
        System.out.println("Desc array, " + length + " element");
        int[] sol = inc(new int[length]);
        array = desc(new int[length]);

        long startTime = System.nanoTime();
        qcs.sort(array,0, array.length-1);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        assertArrayEquals(array,sol);
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void quickSort_rand(int length) {
        System.out.println("Random array, " + length + " element");
        int[] sol = inc(new int[length]);
        array = rand(new int[length]);

        long startTime = System.nanoTime();
        qcs.sort(array,0, array.length-1);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        assertArrayEquals(array,sol);
    }

    @AfterEach
    public void summary() {
        for (Long time:performance) {
            System.out.println("Mili sec: " + time/1000 + " nano: " + time%1000);
        }
        performance.clear();
    }
}