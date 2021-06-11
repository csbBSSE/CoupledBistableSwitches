## This file discretizes RACIPE states, calculates phases for each parameter set and calculates the linkstrengths for each parameter set.

library(tidyverse)

## discretizes a vector around the weighted mean of the vector 
discret <- function(x, w = 0.5){
    mx <- sum(x*w)/sum(w)
    sx <- sqrt(sum(w*(x-mx)^2)/sum(w))
    x <- (x-mx)/sx
    ifelse(x>0, 1, 0)
}

## reads the RACIPE parameter file and assigns column names to the parameter data frame
readParams <- function(topoFile)
{
    net <- topoFile %>% str_remove(".topo")
    df <- read.delim(paste0(net, "_parameters.dat"), header = F)
    pars <- read.delim(paste0(net, ".prs"), stringsAsFactors = F)
    pars <- pars$Parameter
    colnames(df) <- c("ParID", "nStates", pars)
    return(df)
}

## Calculates the linkstrength for each parameter set
linkStrengthCalc <- function(topoFile)
{
    df <- readParams(topoFile)
    topoDf <- read.delim(topoFile, sep = " ", stringsAsFactors = F)
    par_new <- apply(df, 1, function(x){#browser()
        x <- x[-c(1,2)]
        linkStrengths <- apply(topoDf, 1, function(y){
            Source <- y[1]
            Target <- y[2]
            Type <- as.integer(y[3])
            g <- x[paste0("Prod_of_", Source)]
            k <- x[paste0("Deg_of_", Source)]
            n <- x[paste0("Num_of_", Source, "To", Target)]
            l <- ifelse(Type == 1, "Act", "Inh")
            l <- x[paste0(l, "_of_", Source, "To", Target)]
            h0 <- x[paste0("Trd_of_", Source, "To", Target)]
            g*n/(l*h0*k)
        })
        return(linkStrengths)
    }) %>% t %>% data.frame %>% set_names(links) %>% mutate(nStates = df$nStates)
    write.csv(par_new, str_replace(topoFile, ".topo", "linkStrength.csv"), row.names = F)
    return(par_new)
    
}

## Compiles all RACIPE solutions into a single file
solutionCompile <- function(topoFile)
{
    net <- topoFile %>% str_remove(".topo")
    solutionFiles <- list.files(".", "solution_")
    solutionLengths <- sapply(solutionFiles, function(x){
        length(readLines(x))
    })
    bads <- which(solutionLengths < 2)
    solutionFiles <- solutionFiles[-bads]
    pars <- read.delim(paste0(net, ".prs"), stringsAsFactors = F)
    pars <- pars$Parameter
    nodes <- pars[which(str_detect(pars, "Prod"))] %>% str_remove("Prod_of_")
    nNodes <- length(nodes)
    compiled <- lapply(solutionFiles, function(x){
        df <- read_delim(x, delim = "\t", col_names = F)
        dfextra <- df[, 1:2]
        dfStates <- df[, -(1:2)]
        colz <- 1:ncol(dfStates)
        nStates <- length(colz)/nNodes
        dfextra$relStab <- 1/nStates
        colz <- split(colz, ceiling(seq_along(colz)/nNodes))
        df <- lapply(colz, function(y){
            cbind.data.frame(dfextra, dfStates[, y])
        }) %>% reuce(rbind.data.frame)
    }) %>% reduce(rbind.data.frame) %>% 
        set_names(c("ParID", "nStates", "RelStab", nodes)) %>%
        mutate(ParID = as.integer(ParID)) %>%
        arrange(ParID)
    write_delim(compiled, paste0(net, "_solution.dat"), delim = "\t")
}

## calculates the phases for each parameter set, using the compiled solution file
phaseCalc <- function(topoFile, gk = F)
{
    params <- readParams(topoFile)
    nodes <- colnames(params)
    nodes <- nodes[str_detect(nodes, "Prod")] %>% str_remove("Prod_of_")
    
    solnFile <- paste0(str_remove(topoFile, ".topo"), "_solution.dat")
    if(!file.exists(solnFile))
        solutionCompile(topoFile)
    solnDf <- read.delim(solnFile, header = F) %>% 
        set_names(c("ParID", "nStates", "RelStab", nodes))
    
    solnDf[, nodes] <- solnDf %>% select(nodes) %>% sapply(function(x){
        discret(x, solnDf$RelStab)
    })
    solnDf <- solnDf %>% unite("State", nodes, sep = "") %>% group_by(ParID) %>%
        summarise(Phase = paste0(unique(State), collapse = "-"))
    params <- merge(params, solnDf, by = "ParID", all = T)
    nam <- str_remove(topoFile, ".topo")
    nam <- paste0(nam, "_phases.csv")
    write.csv(params, nam, row.names = F)
    return(params)
}

## Function calls
phaseCalc(topoFile)
linkStrengthCalc(topoFile)

