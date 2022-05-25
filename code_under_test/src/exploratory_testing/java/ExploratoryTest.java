import search.binary_search.BinarySearch;
import search.exponential_search.ExponentialSearch;
import search.fibonacci_search.FibonacciSearch;
import search.interpolation_search.Interpolation;
import search.jump_search.JumpSearch;
import search.linear_search.LinearSearch;

import java.util.*;


public class ExploratoryTest {
    private static final String[] methods = new String[]{
            "BinarySearch",
            "ExponentialSearch",
            "FibonacciSearch",
            "Interpolation",
            "JumpSearch",
            "LinearSearch"
    };

    private static int chooseSearchMethod(Scanner sc)
    {

        System.out.println("INTERACTIVE MANUAL TEST OF SEARCH FUNCTIONS\n-----------------------------------------");
        while (true)
        {
            System.out.println("Choose search method: [1-6]");
            for (int i = 0; i < methods.length; i++)
                System.out.println((i+1) + " " + methods[i]);
            int num = sc.nextInt();
            if (num <= 6 && num >= 1)
                return num;
            else
                System.out.println("Invalid number. Try again!");
        }
    }

    private static int getSizeAndElements(Scanner sc, List<Integer> array)
    {
        int n;
        while (true)
        {
            System.out.print("Array size (n>0): ");
            n = sc.nextInt();
            if (n <= 0)
                System.out.println("Invalid size!");
            else
                break;
        }
        System.out.println("Provide " + n + " integer values, separated by newlines:");
        for (int i = 0; i < n; i++)
        {
            Integer a = sc.nextInt();
            array.add(a);
        }
        return n;
    }

    private static int getElementToFind(Scanner sc) {
        System.out.print("Provide the element to find: ");
        return sc.nextInt();
    }

    private static void testBinarySearch(int n, int[] array, int toFind)
    {
        long s, t;
        s = System.nanoTime() / 1000;
        int res = BinarySearch.binarySearch(array, 0, n-1, toFind);
        t = System.nanoTime() / 1000;
        System.out.println("Search has run for " + (t - s) + " microseconds");
        if (res == -1)
            System.out.println("Value not found");
        else
            System.out.println("Value found at pos. " + res);
    }

    private static void testExponentialSearch(int n, int[] array, int toFind)
    {
        long s, t;
        s = System.nanoTime() / 1000;
        int res = ExponentialSearch.exponentialSearch(array,  n, toFind);
        t = System.nanoTime() / 1000;
        System.out.println("Search has run for " + (t - s) + " microseconds");
        if (res < 0)
            System.out.println("Value not found");
        else
            System.out.println("Value found at pos. " + res);
    }

    private static void testFibonacciSearch(int n, int[] array, int toFind)
    {
        long s, t;
        var fs = new FibonacciSearch();
        var arr = Arrays.stream(array).boxed().toArray(Integer[]::new);
        s = System.nanoTime() / 1000;
        int res = fs.find(arr, (Integer)toFind);
        t = System.nanoTime() / 1000;
        System.out.println("Search has run for " + (t - s) + " microseconds");
        if (res == -1)
            System.out.println("Value not found");
        else
            System.out.println("Value found at pos. " + res);
    }

    private static void testInterpolationSearch(int n, int[] array, int toFind)
    {
        long s, t;
        s = System.nanoTime() / 1000;
        int res = Interpolation.interpolationSearch(array,  toFind);
        t = System.nanoTime() / 1000;
        System.out.println("Search has run for " + (t - s) + " microseconds");
        if (res == -1)
            System.out.println("Value not found");
        else
            System.out.println("Value found at pos. " + res);
    }

    private static void testJumpSearch(int n, int[] array, int toFind)
    {
        long s, t;
        s = System.nanoTime() / 1000;
        int res = JumpSearch.SearchJump(array,  toFind);
        t = System.nanoTime() / 1000;
        System.out.println("Search has run for " + (t - s) + " microseconds");
        if (res == -1)
            System.out.println("Value not found");
        else
            System.out.println("Value found at pos. " + res);
    }

    private static void testLinearSearch(int n, int[] array, int toFind)
    {
        long s, t;
        s = System.nanoTime() / 1000;
        int res = LinearSearch.linearSearch(array,  toFind);
        t = System.nanoTime() / 1000;
        System.out.println("Search has run for " + (t - s) + " microseconds");
        if (res == -1)
            System.out.println("Value not found");
        else
            System.out.println("Value found at pos. " + res);
    }

    public static void main(String[] args)
    {
        Scanner sc = new Scanner(System.in);
        int method = chooseSearchMethod(sc);
        List<Integer> array = new ArrayList<Integer>();
        int n = getSizeAndElements(sc, array);
        int[] arr = array.stream().mapToInt(i -> i).toArray();
        System.out.println("Sorting array by ascending order");
        Collections.sort(array);
        int toFind = getElementToFind(sc);
        System.out.println("EXECUTING SEARCH METHOD: " + methods[method-1]);
        switch (method) {
            case 1 -> testBinarySearch(n, arr, toFind);
            case 2 -> testExponentialSearch(n, arr, toFind);
            case 3 -> testFibonacciSearch(n, arr, toFind);
            case 4 -> testInterpolationSearch(n, arr, toFind);
            case 5 -> testJumpSearch(n, arr, toFind);
            default -> testLinearSearch(n, arr, toFind);
        }
        // Fail: fibonacci
        // Input:
        // (9, 3, 2, 1, 4, 6, 8, 5, 4, 7), toFind = 78
        // Stack trace:
        // Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 10 out of bounds for length 10
        //	at search.fibonacci_search.FibonacciSearch.find(FibonacciSearch.java:52)
        //	at ExploratoryTest.testFibonacciSearch(ExploratoryTest.java:96)
        //	at ExploratoryTest.main(ExploratoryTest.java:158)
    }
}
