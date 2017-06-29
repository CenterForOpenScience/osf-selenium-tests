package buildingBlocks;

import java.net.URL;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

public class CreateProjectChrome {
	public static void main(String args[]) throws Exception{
		DesiredCapabilities caps = new DesiredCapabilities();
		caps.setCapability("browser", "Chrome");
		caps.setCapability("browser_version", "58.0");
		caps.setCapability("os", "Windows");
		caps.setCapability("os_version", "10");
		caps.setCapability("resolution", "1024x768");
			
		 WebDriver wd = new RemoteWebDriver(
		    	    new URL("https://shikhadubey1:Mhtt1XkQq18k8nqQzsqn@hub-cloud.browserstack.com/wd/hub"),
		    	    DesiredCapabilities.chrome()
		    	  );
		 wd.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
		    wd.get("https://staging.osf.io/");  //go to the link
	    
	    wd.findElement(By.xpath("/html/body/div[2]/nav/div/div[2]/ul/li[4]/div/a[2]")).click();
	    
		WebElement email= wd.findElement(By.xpath("/html/body/div/div[1]/div[1]/form/section[1]/input"));
		email.sendKeys("osframeworktesting+ghost@gmail.com");
		Thread.sleep(5000);
		WebElement password= wd.findElement(By.id("password"));
		password.sendKeys("\"Repr0duce!\"");
		Thread.sleep(6000);
		if ( wd.findElement(By.id("rememberMe")).isSelected() )
	    {
	         wd.findElement(By.id("rememberMe")).click();
	    }
		Thread.sleep(5000);
		wd.findElement(By.xpath("/html/body/div/div[1]/div[1]/form/section[3]/input[4]")).click();
		Thread.sleep(6000);
		wd.findElement(By.xpath("/html/body/div[4]/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/button")).click();
		Thread.sleep(6000);
		wd.findElement(By.name("projectName")).sendKeys("Testselenium");
		Thread.sleep(4000);
		wd.findElement(By.xpath("/html/body/div[4]/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/div/div/div/div[3]/button[2]")).click();
		Thread.sleep(4000);
		wd.findElement(By.xpath("/html/body/div[4]/div[2]/div/div/div/div/div[1]/m-b-lg/div/span/div/div/div/div/div[2]/a")).click();
		System.out.println(wd.getTitle());
		wd.findElement(By.xpath("/html/body/div[4]/div/div[1]/header/nav/div/div[2]/ul/li[8]/a")).click();  //project settings
	   
		
		Thread.sleep(8000);
		wd.findElement(By.xpath("/html/body/div[4]/div/div[4]/div[2]/div[1]/div[2]/button[3]")).click(); // Click delete
	    Thread.sleep(6000);
	    String OSNAMES= wd.findElement(By.xpath("/html/body/div[6]/div/div/div[2]/div/p[2]")).getText();
	    String[] parts = OSNAMES.split(" ");
	    String OS = parts[5];
	   wd.findElement(By.id("bbConfirmText")).sendKeys(OS);
	   Thread.sleep(6000);
	    wd.findElement(By.xpath("/html/body/div[6]/div/div/div[3]/button[2]")).click();
	    Thread.sleep(6000);
	    // logout process
	  wd.findElement(By.xpath("/html/body/div[2]/nav/div/div[2]/ul/li[5]/a")).click();  // settings
	  Thread.sleep(6000);
	 wd.findElement(By.xpath("/html/body/div[2]/nav/div/div[2]/ul/li[5]/ul/li[4]/a")).click();
	    Thread.sleep(6000);
	    wd.quit();
	    
	}
}

//this is just a comment to check if my source tree is working fine---  Shikha Dubey
