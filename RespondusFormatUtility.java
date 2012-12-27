/*
 * This program will format a test with answer key 
 * for use with Respondus
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

public class RespondusFormatUtility {

    public static void main(String[] args) throws FileNotFoundException, IOException {
        Scanner getfile = new Scanner(System.in);
        System.out.println("Enter the full name and path of file to convert:");
        File rawTest = new File(getfile.nextLine());
        String input = new Scanner(rawTest).useDelimiter("\\Z").next();
        Pattern p = Pattern.compile("(Answer:|\\bAnswer\\b|ANS:)(.*)", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(input);
        StringBuffer questionList = new StringBuffer();
        ArrayList<String> answerList = new ArrayList<>();
        int number = 0;
        while (m.find()) {
            number += 1;
            //System.out.println("Found: " + m.group(1) + m.group(2));
            if (m.group(2).contains("TRUE") || (m.group(2).contains("FALSE"))) {
                m.appendReplacement(questionList, "A) True\r\nB) False\r\n");
            } else {
                m.appendReplacement(questionList, "");
            }
            answerList.add(number + "." + m.group(2).replaceAll("%.*", ""));
        }
        System.out.println();
        String cleanedQuestionList = questionList.toString().replaceAll("Diff:.*|Topic:.*|Skill:.*|Geog Standards:.*|Bloom's Taxonomy:.*", "");
        String footer = "\n";
        String delim = "\n";
        StringBuilder test = new StringBuilder();
        System.out.println(cleanedQuestionList);
        System.out.println("Answers:");
        for (String answer : answerList) {
            test.append(answer).append(delim);
        }
        System.out.println(toProperCase(test.append(footer).toString()));
        Writer bw = null;
        File file = new File("formatted_test.txt");
        bw = new BufferedWriter(new FileWriter(file));
        bw.write(cleanedQuestionList);
        bw.write("\r\nAnswers:\n");
        for (String answer : answerList) {
            bw.write("\r\n");
            bw.write(toProperCase(answer));
        }
        bw.close();
    }

    public static String toProperCase(String theString) throws IOException {
        StringReader in = new StringReader(theString.toLowerCase());
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
