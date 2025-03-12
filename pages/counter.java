import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
* @author evivehealth on 08/02/19.
*/
// Java program depicting
// concurrent programming in action.

// Runnable Class that defines the logic
// of run method of runnable interface
public class Counter implements Runnable
{
	private final MainApp mainApp;
	private final int loopLimit;
	private final String task;

	// Constructor to get a reference to the main class
	public Counter
		(MainApp mainApp, int loopLimit, String task)
	{
		this.mainApp = mainApp;
		this.loopLimit = loopLimit;
		this.task = task;
	}

	// Prints the thread name, task number and
	// the value of counter
	// Calls pause method to allow multithreading to occur
	@Override
	public void run()
	{
		for (int i = 0; i < loopLimit; i++)
		{
			System.out.println("Thread: " +
			Thread.currentThread().getName() + " Counter: "
							+ (i + 1) + " Task: " + task);
			mainApp.pause(Math.random());
		}
	}
}
class MainApp
{

	// Starts the threads. Pool size 2 means at any time
	// there can only be two simultaneous threads
	public void startThread()
	{
		ExecutorService taskList =
						Executors.newFixedThreadPool(2);
		for (int i = 0; i < 5; i++)
		{
			// Makes tasks available for execution.
			// At the appropriate time, calls run
			// method of runnable interface
			taskList.execute(new Counter(this, i + 1,
									"task " + (i + 1)));
		}

		// Shuts the thread that's watching to see if
		// you have added new tasks.
		taskList.shutdown();
	}

	// Pauses execution for a moment
	// so that system switches back and forth
	public void pause(double seconds)
	{
		try
		{
			Thread.sleep(Math.round(1000.0 * seconds));
		}
		catch (InterruptedException e)
		{
			e.printStackTrace();
		}
	}

	// Driver method
	public static void main(String[] args)
	{
		new MainApp().startThread();
	}
}
