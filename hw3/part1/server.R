require(datasets)
require(googleVis)
require(shiny)
require(sqldf)

data <- read.csv("cleaned-cdc-mortality-1999-2010-2.csv", header = TRUE)
names(data) <- gsub(x = names(data), pattern = "\\.", replacement = "_")

selected_cause <- "Diseases of the nervous system"

shinyServer(function(input, output) {

  # the hard coded one:
  causeOfDeathFunc <- reactive({
    input$CauseOfDeath
  })
  
  get_the_data <- function(){
    sqldf(paste("select * from data where ICD_Chapter = '", causeOfDeathFunc() ,"' and Year = 2010 and State != 'DC' ", sep=""))
  }
  
  get_distinct_2010_causes <- function(){
    sqldf(paste("select distinct(ICD_Chapter) as cause_of_death from data where Year = 2010 and State != 'DC' ", sep=""))
  }
  
  output$CauseOfDeathHeader <- renderText({
    causeOfDeathFunc()
  })
  
  output$gvis <- renderGvis({
    
    data <- get_the_data()
    
    states <- data.frame(state.abb, state.name)
    colnames(states) <- c("state_abbr","state_name")
    if(nrow(data) >= 50){
      data$StateAbbr <- states$state_abbr
      gvisGeoChart(data, "StateAbbr", "Crude_Rate", options=list(region="US", displayMode="regions", resolution="provinces", width=600, height=400))
    }else{
      # couldn't load, not enough data
    }

  })
})