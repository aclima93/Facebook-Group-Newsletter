package inc.bugs;


import com.google.gson.Gson;
import generated.Smartphone;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import javax.jms.*;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import java.io.*;
import java.math.BigDecimal;
import java.net.SocketTimeoutException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Locale;

public class WebCrawler {

    private static ArrayList<Smartphone> collectedSmartphones = new ArrayList<Smartphone>();
    private static ArrayList<String> createdXMLFiles = new ArrayList<String>();

    public static void main(String[] args){

        jsonFileDir = args[0];

        // create XML file(s)
        createAndSaveXMLFiles();

        // send XML message(s) to the JMS Topic
        publishXMLFilesToJMSTopic();
    }

    /**
     * Creates XML files and saves them just in case
     */
    private static void createAndSaveXMLFiles() {

        JAXBContext jaxbContext;
        Marshaller marshaller;

        try {

            jaxbContext = JAXBContext.newInstance(Smartphone.class);
            marshaller = jaxbContext.createMarshaller();
            marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

            for(Smartphone smartphone : collectedSmartphones) {

                StringWriter stringWriter = new StringWriter();
                marshaller.marshal(smartphone, stringWriter);
                createdXMLFiles.add(stringWriter.toString());
                stringWriter.flush();
            }

        } catch (JAXBException e) {
            // could not create Marshalled XML
            e.printStackTrace();
        }

        if(VERBOSE){
            System.out.println("Created and saved XML files from crawling.");
        }

    }

    /**
     * Creates a Smartphone object from the data in doc
     * @param doc HTML page of smartphone
     */
    private static Smartphone createSmartphone(String url, Document doc) {

        Smartphone smartphone = new Smartphone();

        // URL
        smartphone.setUrl(url);

        Smartphone.TechnicalData technicalData = new Smartphone.TechnicalData();

        // Name and Brand
        Elements pageTitle = doc.select("h1[class=pageTitle]");

        smartphone.setName(pageTitle.select("span[itemprop=name]").text());
        smartphone.setBrand(pageTitle.select("span[itemprop=brand]").text());

        // Price and Currency
        try {

            String[] priceAndCurrency = doc.select("div[class=currentPrice]").select("ins[itemprop=price]").text().replace("\u00a0", " ").split("\\s+"); // pesky &no-break space
            NumberFormat nf = NumberFormat.getInstance(Locale.GERMAN); // German locale has the same decimal and grouping separators as PT
            smartphone.setPrice( new BigDecimal(nf.parse(priceAndCurrency[0]).toString()));
            smartphone.setCurrency(priceAndCurrency[1]);

        } catch (ParseException e) {
            // invalid number format/unparsable number
            if(VERBOSE) {
                e.printStackTrace();
            }
        }

        // Summary Data
        smartphone.setSummaryData(doc.select("ul[class=customList],ul[itemprop=description]").text());

        if(DEBUG_SMARTPHONE) {
            System.out.println("\n\nSmartphone");
            System.out.println("Url: " + smartphone.getUrl());
            System.out.println("Name: " + smartphone.getName());
            System.out.println("Brand: " + smartphone.getBrand());
            System.out.println("Price: " + smartphone.getPrice());
            System.out.println("Currency: " + smartphone.getCurrency());
            System.out.println("Summary: \n" + smartphone.getSummaryData());
        }

        // Technical Data
        Elements tablesFromDoc = doc.select("table[class=simpletable]");
        for(Element tableFromDoc : tablesFromDoc){

            Smartphone.TechnicalData.Table table = new Smartphone.TechnicalData.Table();
            table.setTableTitle(tableFromDoc.select("caption").text());

            if(DEBUG_SMARTPHONE) {
                System.out.println("\nTable");
                System.out.println("TableTitle: " + table.getTableTitle());
            }

            for(Element rowfromTable : tableFromDoc.select("tbody").select("tr")) {

                Smartphone.TechnicalData.Table.TableData tableData = new Smartphone.TechnicalData.Table.TableData();

                tableData.setDataName(rowfromTable.select("th").text());
                tableData.setDataValue(rowfromTable.select("td").text());

                if(DEBUG_SMARTPHONE) {
                    System.out.println("TableData name: " + tableData.getDataName());
                    System.out.println("TableData value: " + tableData.getDataValue());
                }

                table.getTableData().add( tableData);
            }

            technicalData.getTable().add(table);
        }
        if(!technicalData.getTable().isEmpty()) {
            smartphone.setTechnicalData(technicalData);
        }

        return smartphone;
    }

}
