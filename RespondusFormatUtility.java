/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
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
import java.io.Writer;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.*;

public class RespondusFormatUtility {

    public static void main(String[] args) throws FileNotFoundException, IOException {

        Scanner getfile = new Scanner(System.in);
        System.out.println("Enter the full name and path of file to convert:");
        // read in the test file
        File rawTest = new File(getfile.nextLine());
        String input = new Scanner(rawTest).useDelimiter("\\Z").next();

        // find answer key pattern
        Pattern p = Pattern.compile("(Answer:|ANSWER:|ANS:)(.*)");
        Matcher m = p.matcher(input);

        // store questions
        StringBuffer questionList = new StringBuffer();

        // store answer key
        ArrayList<String> answerList = new ArrayList<>();

        // distinguish questions from answer key, and number answer key   
        int number = 0;
        while (m.find()) {
            number += 1;
            System.out.println("Found: " + m.group(1) + m.group(2));
            m.appendReplacement(questionList, "");

            //replace any extra comments or feedback data in the answer list
            answerList.add(number + "." + m.group(2).replaceAll("%.*", ""));

        }
        //m.appendTail(questionList); will append whatever followed the last match  
        System.out.println();

        // clear extra comments or feedback data from test questions
        String cleanedQuestionList = questionList.toString().replaceAll("Diff:.*|Topic:.*|Skill:.*|Geog Standards:.*|Bloom's Taxonomy:.*", "");

        // print to console
        //String header = "\n";
        String footer = "\n";
        String delim = "\n";
        StringBuilder test = new StringBuilder();
        System.out.println(cleanedQuestionList);
        System.out.println("Answers:");
        for (String answer : answerList) {
            test.append(answer).append(delim);

        }
        System.out.println(test.append(footer).toString());

        // Print to file
        Writer bw = null;
        File file = new File("formatted_test.txt");

        bw = new BufferedWriter(new FileWriter(file));
        bw.write(cleanedQuestionList);

        bw.write("\r\nAnswers:\n");
        for (String answer : answerList) {
            bw.write("\r\n");
            bw.write(answer);
        }
        bw.close();
    }
}