using System;
using System.Collections.Generic;

namespace FileExtensionInfoApp
{
    class Program
    {
        static void Main(string[] args)
        {
            // Using Dictionary for saving extension  format and information details as key value pair
            Dictionary<string, string> fileExtensions = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
            {
                { ".txt",  "Plain text file – contains readable text." },
                { ".doc",  "Microsoft Word 97-2003 document." },
                { ".docx", "Microsoft Word Open XML document." },
                { ".pdf",  "Portable Document Format – fixed-layout document." },
                { ".xls",  "Microsoft Excel 97-2003 spreadsheet." },
                { ".xlsx", "Microsoft Excel Open XML spreadsheet." },
                { ".ppt",  "PowerPoint 97-2003 presentation." },
                { ".pptx", "PowerPoint Open XML presentation." },
                { ".jpg",  "JPEG image file – compressed photo." },
                { ".jpeg", "JPEG image file – compressed photo." },
                { ".png",  "PNG image – lossless compressed image." },
                { ".gif",  "GIF image – supports animation." },
                { ".mp3",  "MP3 audio file – compressed sound/music." },
                { ".wav",  "WAV audio file – uncompressed or lossless audio." },
                { ".mp4",  "MP4 video file – very common video format." },
                { ".mov",  "QuickTime movie file – Apple video format." },
                { ".avi",  "AVI video file – older Windows video format." },
                { ".mkv",  "Matroska video file – supports multiple streams." },
                { ".webm", "WebM video file – optimized for the web." },
                { ".zip",  "ZIP compressed archive – contains multiple files." },
                { ".rar",  "RAR compressed archive – proprietary format." },
                { ".exe",  "Windows executable program file." },
                { ".html", "HTML web page file." },
                { ".css",  "Cascading Style Sheet – styles for web pages." }
            };

            Console.WriteLine("=== File Extension Information System ===");
            Console.WriteLine("=========================================\n");

            while (true)
            {
                Console.Write("Enter a file extension(ex '.mp4' or 'mp4' any format works)\nor enter 'list' to check list of supported file formats\nor enter exit to close program:");
                string input = Console.ReadLine();

                if (input == null)
                {
                    Console.WriteLine("No input detected. Please try again.\n");
                    continue;
                }

                input = input.Trim();

                // Exit option
                if (input.Equals("exit", StringComparison.OrdinalIgnoreCase))
                {
                    Console.WriteLine("Exiting the program. Goodbye!");
                    break;
                }

                // Show all supported extensions
                if (input.Equals("list", StringComparison.OrdinalIgnoreCase))
                {
                    Console.WriteLine("\nSupported file extensions:");
                    foreach (var key in fileExtensions.Keys)
                    {
                        Console.WriteLine($"  {key}");
                    }
                    Console.WriteLine();
                    continue;
                }

                // Handle empty input gracefully
                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine("You didn't enter anything. Please type a file extension.\n");
                    continue;
                }

                // Add . in fromt of format if user doesnt provide dot in front
                if (!input.StartsWith("."))
                {
                    input = "." + input;
                }

                // Check for extension formatL
                if (fileExtensions.TryGetValue(input, out string description))
                {
                    Console.WriteLine($"\nExtension: {input}");
                    Console.WriteLine($"Description: {description}\n");
                }
                else
                {
                    // Graceful handling of unexpected / unsupported extensions
                    Console.WriteLine($"\nNo information about this format '{input}'.");
                    Console.WriteLine("Please try another extension or type 'list' to see supported file formats.\n");
                }
            }
        }
    }
}
