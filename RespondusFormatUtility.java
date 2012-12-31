/*
 * This program will format a test with answer key 
 * for use with Respondus
 * 
 */
package respondus.format.utility;

/**
 *
 * @author Gary
 */
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.*;
import javax.swing.JOptionPane;

public class RespondusFormatUtility {

    public static void main(String[] args) throws FileNotFoundException, IOException {

        Object getFile = JOptionPane.showInputDialog("Test to Format", "Enter name of text file (i.e. astronomy101.txt)");
        String theFile = (String) getFile;
        File file = new File(theFile);
        if (!theFile.endsWith(".txt")) {
            System.out.println("Usage: This is not a text file!");
            System.exit(0);
        } else if (!file.exists()) {
            System.out.println("File not found!");
            System.exit(0);
        }
        //Scanner inputFile = new Scanner(System.in);
        //System.out.println("Enter the full name and path of file to convert:");
        //File testFile = new File(inputFile.nextLine());
        String rawTest = new Scanner(file).useDelimiter("\\Z").next();
        StringBuffer questionList = new StringBuffer();
        ArrayList<String> answerList = new ArrayList<>();
        formatTest(rawTest, questionList, answerList);
    }

    public static void formatTest(String rawTest, StringBuffer questionList, ArrayList answerList) throws IOException {

        Pattern feedbackTerms = Pattern.compile("Diff:.*|Topic:.*|Skill:.*|Geog Standards:.*|Bloom's Taxonomy:.*");
        Pattern ansKey = Pattern.compile("(^Answer|\nAnswer|Answer:|ANS:)(.*)", Pattern.CASE_INSENSITIVE);
        Matcher m = ansKey.matcher(rawTest);

        int number = 0;
        while (m.find()) {
            number += 1;
            //System.out.println("Found: " + m.group(1) + m.group(2));
            if (m.group(2).contains("TRUE") || (m.group(2).contains("FALSE"))) {
                m.appendReplacement(questionList, "\nA) True\r\nB) False\r\n");
            } else {
                m.appendReplacement(questionList, "");
            }
            answerList.add(number + "." + m.group(2).replaceAll(":|%.*", ""));
        }
        String cleanedQuestionList = questionList.toString().replaceAll(feedbackTerms.toString(), "");
        /*
        System.out.println("\nBegin formatted test...\n");        
        String footer = "\n";
        String delim = "\n";
        StringBuilder test = new StringBuilder();
        System.out.println(cleanedQuestionList);
        System.out.println("Answers:");
        for (Object answer : answerList) {
            test.append(answer).append(delim);
        }
        System.out.println(toProperCase(test.append(footer).toString()));
        */
        Writer bw = null;
        Object getSaveFile = JOptionPane.showInputDialog("Give the file a name", "Enter name for formatted test file (i.e myformattedtest.txt");
        String saveFile = (String) getSaveFile;
        File file = new File(saveFile);
        bw = new BufferedWriter(new FileWriter(file));
        bw.write(cleanedQuestionList);
        bw.write("\r\nAnswers:\n");
        for (Object answer : answerList) {
            bw.write("\r\n");
            bw.write(toProperCase(answer));
        }
        bw.close();
    }

    public static String toProperCase(Object object) throws IOException {

        StringReader in = new StringReader(object.toString().toLowerCase());
        boolean precededBySpace = true;
        StringBuilder properCase = new StringBuilder();
        while (true) {
            int i = in.read();
            if (i == -1) {
                break;
            }
            String s = Character.toString((char) (i));
            if (s.matches("[0-9]||[')']|['.']|[' ']")) {
                properCase.append(s);
                precededBySpace = true;
            } else {
                if (precededBySpace) {
                    properCase.append(s.toUpperCase());
                } else {
                    properCase.append(s);
                }
                precededBySpace = false;
            }
        }
        return properCase.toString();
    }
}
