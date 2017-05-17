require(datasets)
require(googleVis)
require(shiny)
library(sqldf)

data <- read.csv("cleaned-cdc-mortality-1999-2010-2.csv", header = TRUE)

names(data) <- gsub(x = names(data), pattern = "\\.", replacement = "_")
# Integers are too small...
data$Population <- as.numeric(data$Population)
usa <- sqldf("select ICD_Chapter, Year, ((sum(Deaths) / sum(Population)) * 100000) as Crude_Rate from data group by ICD_Chapter, Year")
usa$State <- "USA"
usa$Crude_Rate <- round(usa$Crude_Rate, digits = 1)
all_data <- rbind(data[,c("ICD_Chapter","State", "Year", "Crude_Rate")], usa)

shinyServer(function(input, output) {

  stateSelectFunc <- reactive({
    input$StateToCompareTo
  })
  
  causeSelectFunc <- reactive({
    input$CauseOfDeath
  })

  output$statusLabel <- renderText({
    paste("USA and ", stateSelectFunc(), "(",causeSelectFunc(),")")
  })
  
  output$gvis <- renderGvis({
    state_selected <- stateSelectFunc()
    usa_df <- sqldf("select Year, Crude_Rate from all_data where State = 'USA' and ICD_Chapter = 'Certain infectious and parasitic diseases' order by Year ")
    other_query <- paste("select Year, Crude_Rate from all_data where State = '",state_selected,"' and ICD_Chapter = 'Certain infectious and parasitic diseases' order by Year ", sep="")
    other_df <- sqldf(other_query)
    both <- merge(x = usa_df, y = other_df, by = "Year", all = TRUE)
    colnames(both) <- c("Year","USA",state_selected)
    gvisColumnChart(both, xvar="Year", yvar=c("USA",state_selected))
  })
})