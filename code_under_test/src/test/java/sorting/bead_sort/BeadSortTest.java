package sorting.bead_sort;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static sorting.ArraySorter.*;

class BeadSortTest {
    private static BeadSort bds = new BeadSort();
    private int[] array;
    private static final int[] values = {100,1000,10000};
    private static ArrayList<Long> performance = new ArrayList<>();

    @BeforeAll
    public static void introduction() {
        System.out.println(bds.getClass().getName());
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void beadSort_inc(int length) {
        System.out.println("Sorted array, " + length + " element");
        int[] sol = inc(new int[length]);
        array = inc(new int[length]);

        long startTime = System.nanoTime();
        array = bds.beadSort(array);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        assertArrayEquals(array,sol);
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void beadSort_desc(int length) {
        System.out.println("Desc array, " + length + " element");
        int[] sol = inc(new int[length]);
        array = desc(new int[length]);

        long startTime = System.nanoTime();
        array = bds.beadSort(array);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        assertArrayEquals(array,sol);
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void beadSort_rand(int length) {
        System.out.println("Random array, " + length + " element");
        int[] sol = inc(new int[length]);
        array = rand(new int[length]);

        long startTime = System.nanoTime();
        array = bds.beadSort(array);
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