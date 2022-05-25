package sorting.bead_sort;

import org.junit.Assert;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.ArrayList;
import sorting.bead_sort.BeadSort;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static sort_array.ArraySorter.*;

class BeadSortTest {

    private BeadSort bds = new BeadSort();
    private int[] array;
    private static final int[] values = {100,1000,10000};
    private static ArrayList<Long> performance = new ArrayList<>();

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void beadSort_inc(int length) {
        int[] sol = inc(new int[length]);
        array = inc(new int[length]);

        long startTime = System.nanoTime();
        array = bds.beadSort(array);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        Assert.assertArrayEquals(array,sol);
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void beadSort_desc(int length) {
        int[] sol = inc(new int[length]);
        array = desc(new int[length]);

        long startTime = System.nanoTime();
        array = bds.beadSort(array);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        Assert.assertArrayEquals(array,sol);
    }

    @ParameterizedTest
    @ValueSource(ints = {100,1000,10000})
    void beadSort_rand(int length) {
        int[] sol = inc(new int[length]);
        array = rand(new int[length]);

        long startTime = System.nanoTime();
        array = bds.beadSort(array);
        long endTime = System.nanoTime();

        performance.add(endTime - startTime);

        Assert.assertArrayEquals(array,sol);
    }

    @AfterAll
    public static void summary() {
        for (Long time:performance) {
            System.out.println(time);
        }
    }
}