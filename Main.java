
package serializable;

import java.io.IOException;
import java.util.Scanner;
import static java.lang.System.exit;

public class Main 
{
    public static void main(String[] args) throws IOException, ClassNotFoundException
    {
         Scanner cin = new Scanner(System.in);
        String choice;
        while (true)
        {
            System.out.println("what do you want???");
            System.out.println("1.Insert " + "\n" + "2.Update " + "\n" + "3.Search " + "\n" + "4.Print " + "\n" + "5.Exit " );
            choice = cin.nextLine();
            if(choice.equals("1")){
                String RegNo;
                RegNo R1 = new RegNo ();
                System.out.println("Enter the RegNo: ");
                RegNo = cin.nextLine ();
                R1.personCreator(RegNo);
            }
            else if(choice.equals("2")){
                String RegNo;
                RegNo R1 = new RegNo();
                System.out.println("Enter the RegNo: ");
                RegNo =cin.nextLine();
                String name;
                String phoneNo;
                String Roll;
                System.out.print("Name: ");
                name = cin.nextLine();
                System.out.print("Roll: ");
                Roll = cin.nextLine();
                System.out.print("PhoneNo: ");
                phoneNo = cin.nextLine();
                R1.updateObj(name,phoneNo,RegNo,Roll);

            }
            else if(choice.equals("3")){
                String RegNo;
                RegNo R1 = new RegNo();
                System.out.println("Enter the RegNo: ");
                RegNo = cin.nextLine();
                R1.search(RegNo);
            }
            else if(choice.equals("4")){
                RegNo R1 = new RegNo();
                R1.ObjRead();
            }
            else if(choice.equals("5")){
                exit(0);
            }
            else System.out.println("Wrong choice!!!!Enter ur choice again---");
        }
    }
}
