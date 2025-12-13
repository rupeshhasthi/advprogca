using System;
using System.Collections.Generic;

namespace ContactBookApp
{
    public class Contact
    {
        // Fields with encapsulation
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Company { get; set; }
        public string MobileNumber { get; private set; }  // validation inside setter method
        public string Email { get; private set; }          // now validated via SetEmail
        public DateTime Birthdate { get; set; }

        public Contact(string firstName, string lastName, string company,        // Constructor
                       string mobileNumber, string email, DateTime birthdate)
        {
            FirstName = firstName;
            LastName = lastName;
            Company = company;
            SetMobileNumber(mobileNumber);
            SetEmail(email);
            Birthdate = birthdate;
        }

        // Validate mobile number
        public bool SetMobileNumber(string mobile)
        {
            try
            {
                if (!IsValidMobileNumber(mobile))
                    throw new FormatException("Invalid mobile number. It must be a non-zero 9-digit positive number.");

                MobileNumber = mobile;
                return true;
            }
            catch (FormatException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                return false;
            }
        }

        public static bool IsValidMobileNumber(string mobile)
        {
            if (string.IsNullOrWhiteSpace(mobile))
                return false;

            // Must be exactly 9 digits
            if (mobile.Length != 9)
                return false;

            // All characters must be digits
            foreach (char c in mobile)
            {
                if (!char.IsDigit(c))
                    return false;
            }

            // Reject all zeros ("000000000")
            if (mobile == "000000000")
                return false;

            return true;
        }

        // Validate email (simple but solid using MailAddress)
        public bool SetEmail(string email)
        {
            try
            {
                if (!IsValidEmail(email))
                    throw new FormatException("Invalid email format.");

                Email = email;
                return true;
            }
            catch (FormatException ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                return false;
            }
        }

        public static bool IsValidEmail(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
                return false;

            try
            {
                // Uses built-in .NET email parser
                var addr = new System.Net.Mail.MailAddress(email);
                return addr.Address == email;
            }
            catch
            {
                return false;
            }
        }

        public override string ToString()
        {
            return $"{FirstName} {LastName} ({MobileNumber})";
        }

        public string GetFullDetails()
        {
            return $"First Name : {FirstName}\n" +
                   $"Last Name  : {LastName}\n" +
                   $"Company    : {Company}\n" +
                   $"Mobile     : {MobileNumber}\n" +
                   $"Email      : {Email}\n" +
                   $"Birthdate  : {Birthdate:dd MMM yyyy}\n";
        }
    }

    // Creating Class Contact Book with all functions
    public class ContactBook
    {
        private List<Contact> contacts;

        public ContactBook()
        {
            contacts = new List<Contact>();

            // === Preloading 20 Contacts ===
            contacts.Add(new Contact("Emily",  "Blackwell",  "Dublin Business School", "087111111", "emily.blackwell@dbs.ie", new DateTime(1990, 1, 1)));
            contacts.Add(new Contact("John",   "Murphy",     "TechCorp",               "087222222", "john.murphy@techcorp.com",     new DateTime(1985, 5, 12)));
            contacts.Add(new Contact("Sarah",  "O'Brien",    "HealthPlus",             "087333333", "sarah.obrien@hp.ie",           new DateTime(1992, 7, 23)));
            contacts.Add(new Contact("Michael","Daly",       "SkyNet",                 "087444444", "michael.daly@skynet.com",      new DateTime(1988, 3, 15)));
            contacts.Add(new Contact("Laura",  "Walsh",      "EducationHub",           "087555555", "laura.walsh@edu.ie",           new DateTime(1995, 9, 9)));
            contacts.Add(new Contact("Daniel", "Kavanagh",   "BuildIT",                "087666666", "daniel.k@buildit.ie",          new DateTime(1981, 11, 30)));
            contacts.Add(new Contact("Grace",  "Kelly",      "GreenWorld",             "087777777", "grace.kelly@gw.ie",            new DateTime(1993, 4, 19)));
            contacts.Add(new Contact("Tom",    "Byrne",      "CarPlus",                "087888888", "tom.byrne@carplus.ie",         new DateTime(1987, 8, 5)));
            contacts.Add(new Contact("Emma",   "Nolan",      "ShopSmart",              "087999999", "emma.nolan@shopsmart.ie",      new DateTime(1991, 2, 14)));
            contacts.Add(new Contact("James",  "Reilly",     "FinanceNow",             "085111111", "james.reilly@fn.ie",           new DateTime(1984, 6, 8)));

            contacts.Add(new Contact("Hannah", "Moore",      "DBS",                    "085222222", "hannah.moore@dbs.ie",         new DateTime(1996, 12, 25)));
            contacts.Add(new Contact("Kevin",  "Lynch",      "Apple",                  "085333333", "kevin.lynch@apple.com",        new DateTime(1979, 10, 20)));
            contacts.Add(new Contact("Aoife",  "Ryan",       "Microsoft",              "085444444", "aoife.ryan@microsoft.com",     new DateTime(1997, 3, 14)));
            contacts.Add(new Contact("Patrick","Quinn",      "SalesPro",               "085555555", "patrick.quinn@salespro.ie",    new DateTime(1983, 1, 11)));
            contacts.Add(new Contact("Olivia", "Flynn",      "BeautyCare",             "085666666", "olivia.flynn@beauty.ie",       new DateTime(1994, 5, 6)));
            contacts.Add(new Contact("Shane",  "Ward",       "FitLife",                "085777777", "shane.ward@fitlife.ie",        new DateTime(1990, 9, 17)));
            contacts.Add(new Contact("Rachel", "Carroll",    "Foodies",                "085888888", "rachel.carroll@foodies.ie",    new DateTime(1992, 4, 2)));
            contacts.Add(new Contact("Liam",   "O'Connor",   "TechWorld",              "085999999", "liam.oconnor@techworld.ie",    new DateTime(1986, 12, 9)));
            contacts.Add(new Contact("Sophie", "Dunne",      "TravelGo",               "086111111", "sophie.dunne@travelgo.ie",     new DateTime(1998, 7, 1)));
            contacts.Add(new Contact("Mark",   "Fitzgerald", "GameZone",               "086222222", "mark.fitzgerald@gz.ie",        new DateTime(1989, 3, 28)));
        }

        // Add Contact
        public void AddContact()
        {
            Console.WriteLine("=== Add New Contact ===");

            Console.Write("First Name: ");
            string firstName = Console.ReadLine();

            Console.Write("Last Name: ");
            string lastName = Console.ReadLine();

            Console.Write("Company: ");
            string company = Console.ReadLine();

            // Mobile with try-catch handling
            string mobile;
            while (true)
            {
                Console.Write("Mobile Number (9-digit, non-zero): ");
                mobile = Console.ReadLine();

                try
                {
                    if (!Contact.IsValidMobileNumber(mobile))
                        throw new FormatException("Mobile number must be a non-zero, 9-digit, positive number.");

                    break;
                }
                catch (FormatException ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                }
            }

            // Email with validation loop
            string email;
            while (true)
            {
                Console.Write("Email: ");
                email = Console.ReadLine();

                try
                {
                    if (!Contact.IsValidEmail(email))
                        throw new FormatException("Invalid email format.");

                    break;
                }
                catch (FormatException ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                }
            }

            // Birthdate with try-catch handling
            DateTime birthdate;
            while (true)
            {
                Console.Write("Birthdate (e.g. 1 Jan 1990): ");
                string birthdateInput = Console.ReadLine();

                try
                {
                    birthdate = DateTime.Parse(birthdateInput);
                    break;
                }
                catch (FormatException)
                {
                    Console.WriteLine("Error: Invalid date format! Please try again.");
                }
            }

            Contact newContact = new Contact(firstName, lastName, company, mobile, email, birthdate);
            contacts.Add(newContact);

            Console.WriteLine("Contact added successfully!");
        }

        // Show all contacts
        public void ShowAllContacts()
        {
            Console.WriteLine("=== All Contacts ===");

            if (contacts.Count == 0)
            {
                Console.WriteLine("No contacts available.");
                return;
            }

            for (int i = 0; i < contacts.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {contacts[i]}");
            }
        }

        // Show Contact Details from contacts
        public void ShowContactDetails()
        {
            Console.WriteLine("=== Show Contact Details ===");

            if (contacts.Count == 0)
            {
                Console.WriteLine("No contacts to show.");
                return;
            }

            ShowAllContacts();
            int index = ReadContactIndex();
            if (index == -1) return;

            Console.WriteLine();
            Console.WriteLine(contacts[index].GetFullDetails());
        }

        // Update Contact
        public void UpdateContact()
        {
            Console.WriteLine("=== Update Contact ===");

            if (contacts.Count == 0)
            {
                Console.WriteLine("No contacts to update.");
                return;
            }

            ShowAllContacts();
            int index = ReadContactIndex();
            if (index == -1) return;

            Contact c = contacts[index];
            Console.WriteLine("Leave field blank to keep the current value.");
            Console.WriteLine();

            Console.Write($"First Name ({c.FirstName}): ");
            string firstName = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(firstName))
                c.FirstName = firstName;

            Console.Write($"Last Name ({c.LastName}): ");
            string lastName = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(lastName))
                c.LastName = lastName;

            Console.Write($"Company ({c.Company}): ");
            string company = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(company))
                c.Company = company;

            Console.Write($"Mobile Number ({c.MobileNumber}): ");
            string mobile = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(mobile))
            {
                if (!c.SetMobileNumber(mobile))
                {
                    Console.WriteLine("Keeping the old mobile number.");
                }
            }

            Console.Write($"Email ({c.Email}): ");
            string email = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(email))
            {
                if (!c.SetEmail(email))
                {
                    Console.WriteLine("Keeping the old email.");
                }
            }

            Console.Write($"Birthdate ({c.Birthdate:dd MMM yyyy}): ");
            string birthdateInput = Console.ReadLine();
            if (!string.IsNullOrWhiteSpace(birthdateInput))
            {
                try
                {
                    DateTime newBirthdate = DateTime.Parse(birthdateInput);
                    c.Birthdate = newBirthdate;
                }
                catch (FormatException)
                {
                    Console.WriteLine("Error: Invalid date! Keeping the old birthdate.");
                }
            }

            Console.WriteLine("Contact updated successfully!");
        }

        // Delete Contact
        public void DeleteContact()
        {
            Console.WriteLine("=== Delete Contact ===");

            if (contacts.Count == 0)
            {
                Console.WriteLine("No contacts to delete.");
                return;
            }

            ShowAllContacts();
            int index = ReadContactIndex();
            if (index == -1) return;

            Console.WriteLine($"Are you sure you want to delete {contacts[index]}? (y/n)");
            string confirm = Console.ReadLine();
            if (confirm != null && confirm.ToLower() == "y")
            {
                contacts.RemoveAt(index);
                Console.WriteLine("Contact deleted successfully!");
            }
            else
            {
                Console.WriteLine("Delete cancelled.");
            }
        }

        // Read a valid contact index
        private int ReadContactIndex()
        {
            Console.Write("Enter index of the contact number: ");
            string input = Console.ReadLine();

            try
            {
                int number = Convert.ToInt32(input);

                if (number < 1 || number > contacts.Count)
                    throw new ArgumentOutOfRangeException();

                return number - 1; 
            }
            catch (FormatException)
            {
                Console.WriteLine("Error: Please enter a valid number!");
            }
            catch (ArgumentOutOfRangeException)
            {
                Console.WriteLine("Error: Number out of range!");
            }

            return -1;
        }
    }

    // Class Program to display options to choose
    class Program
    {
        static void Main(string[] args)
        {
            ContactBook contactBook = new ContactBook();
            int choice = -1;

            do
            {
                Console.WriteLine("===================================");
                Console.WriteLine("           Main Menu");
                Console.WriteLine("===================================");
                Console.WriteLine("1: Add Contact");
                Console.WriteLine("2: Show All Contacts");
                Console.WriteLine("3: Show Contact Details");
                Console.WriteLine("4: Update Contact");
                Console.WriteLine("5: Delete Contact");
                Console.WriteLine("0: Exit");
                Console.WriteLine("===================================");
                Console.Write("Enter your choice: ");

                string input = Console.ReadLine();
                try
                {
                    choice = Convert.ToInt32(input);
                }
                catch (FormatException)
                {
                    Console.WriteLine("Error: Invalid input! Please enter a number from the menu.");
                    Console.WriteLine();
                    continue;
                }

                Console.WriteLine();

                switch (choice)
                {
                    case 1:
                        contactBook.AddContact();
                        break;
                    case 2:
                        contactBook.ShowAllContacts();
                        break;
                    case 3:
                        contactBook.ShowContactDetails();
                        break;
                    case 4:
                        contactBook.UpdateContact();
                        break;
                    case 5:
                        contactBook.DeleteContact();
                        break;
                    case 0:
                        Console.WriteLine("Exiting the application. Goodbye!");
                        break;
                    default:
                        Console.WriteLine("Invalid choice! Please select from the menu.");
                        break;
                }

                Console.WriteLine();
            } while (choice != 0);
        }
    }
}
