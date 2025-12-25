package com.example.matching_back.controller;

import java.nio.file.Path;

import org.springframework.web.bind.annotation.*;

import com.example.matching_back.record.CV;
import com.example.matching_back.record.Offer;
import com.example.matching_back.service.ParserService;

@RestController
@RequestMapping("/api/parser")
public class ParserController {

    private final ParserService parserService;

    public ParserController(ParserService parserService) {
        this.parserService = parserService;
    }

   @PostMapping("/resume")
    public CV parseResume(@RequestBody String resumeFilePath) {
    Path path = Path.of(resumeFilePath); 
    return parserService.parseResume(path);
}

    @PostMapping("/job")
    public Offer parseJob(@RequestBody String jobText) {
        return parserService.parseJob(jobText);
    }
}
