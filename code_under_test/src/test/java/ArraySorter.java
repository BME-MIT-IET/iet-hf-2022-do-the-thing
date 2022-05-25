package sort_array;

public class ArraySorter {
    public static int[] inc(int[] array) {
        for(int i = 0; i < array.length;i++) {
            array[i] = i;
        }
        return array;
    }

    public static int[] desc(int[] array) {
        int length = array.length;
        for(int i = 0; i < length;i++) {
            array[i] = length - i -1;
        }
        return array;
    }

    public static int[] rand(int[] array) {
        for(int i = 0; i < array.length;i++) {
            array[i] = i;
        }
        return array;
    }
}
