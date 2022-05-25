import search.binary_search.BinarySearch;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;


public class ExploratoryTest {
    private static int chooseSearchMethod(Scanner sc)
    {
        String[] methods = new String[]{
                "BinarySearch",
                "ExponentialSearch",
                "FibonacciSearch",
                "Interpolation",
                "JumpSearch",
                "LinearSearch"
        };
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

    private static void testBinarySearch(int n, List<Integer> array, int toFind)
    {
        var bs = new BinarySearch();
    }

    private static void testExponentialSearch(int n, List<Integer> array, int toFind)
    {

    }

    private static void testFibonacciSearch(int n, List<Integer> array, int toFind)
    {

    }

    private static void testInterpolationSearch(int n, List<Integer> array, int toFind)
    {

    }

    private static void testJumpSearch(int n, List<Integer> array, int toFind)
    {

    }

    private static void testLinearSearch(int n, List<Integer> array, int toFind)
    {

    }

    public static void main(String[] args)
    {
        Scanner sc = new Scanner(System.in);
        int method = chooseSearchMethod(sc);
        List<Integer> array = new ArrayList<Integer>();
        int n = getSizeAndElements(sc, array);
        Collections.sort(array);
        int toFind = getElementToFind(sc);
        switch (method) {
            case 1 -> testBinarySearch(n, array, toFind);
            case 2 -> testExponentialSearch(n, array, toFind);
            case 3 -> testFibonacciSearch(n, array, toFind);
            case 4 -> testInterpolationSearch(n, array, toFind);
            case 5 -> testJumpSearch(n, array, toFind);
            default -> testLinearSearch(n, array, toFind);
        }
    }


}
