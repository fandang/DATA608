require(shiny)

shinyUI(pageWithSidebar(
  headerPanel("HW 3A: States by crude mortality for each cause of death"),
  sidebarPanel(
    selectInput("CauseOfDeath", label = h3("Cause Of Death:"),  choices = list(
      "Certain conditions originating in the perinatal period",
      "Certain infectious and parasitic diseases",
      "Congenital malformations, deformations and chromosomal abnormalities",
      "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism",
      "Diseases of the circulatory system",
      "Diseases of the digestive system",
      "Diseases of the genitourinary system",
      "Diseases of the musculoskeletal system and connective tissue",
      "Diseases of the nervous system",
      "Diseases of the respiratory system",
      "Endocrine, nutritional and metabolic diseases",
      "External causes of morbidity and mortality",
      "Mental and behavioural disorders",
      "Neoplasms",
      "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified"), 
      selected = "Neoplasms"),
      em("Cause of death with missing US States were excluded.") 
    
  ),
  mainPanel(
    h3(textOutput("CauseOfDeathHeader")), 
    htmlOutput("gvis")
  )
)
)