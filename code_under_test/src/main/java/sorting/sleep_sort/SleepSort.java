package sorting.sleep_sort;/* Part of Cosmos by OpenGenus Foundation */
import java.util.concurrent.CountDownLatch;
public class SleepSort {
	public static void sleepSortAndPrint(int[] nums){
		final CountDownLatch doneSignal = new CountDownLatch(nums.length);
		for (final int num : nums) {

			Runnable task = () -> {
				doneSignal.countDown();
				try {
					doneSignal.await();

					//using straight milliseconds produces unpredictable
					//results with small numbers
					//using 1000 here gives a nifty demonstration
					Thread.sleep((long)num * 1000);
					System.out.println(num);
				} catch (InterruptedException e) {}
			};

			new Thread(task).start();
		}
	}
	public static void main(String[] args) {
		int[] nums = new int[args.length];
		for (int i = 0; i < args.length; i++)
			nums[i] = Integer.parseInt(args[i]);
		sleepSortAndPrint(nums);
	}
}
