package com.example.matching_back.controller;

import com.example.matching_back.service.*;
import com.example.matching_back.record.CV;
import com.example.matching_back.record.Offer;
import org.springframework.web.bind.annotation.*;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/match")
@CrossOrigin(origins = "http://localhost:4200")
public class MatchController {

    private final ParserService parserService;
    private final MatchingService matchingService;

    public MatchController(ParserService parserService, MatchingService matchingService) {
        this.parserService = parserService;
        this.matchingService = matchingService;
    }

    @PostMapping(value = "/resume-job", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<Map<String, Object>> matchResumeWithJob(
        @RequestParam("file") MultipartFile file,
        @RequestParam("jobText") String jobText) {

    try {
        Path tempFile = Files.createTempFile("upload-", file.getOriginalFilename());
        file.transferTo(tempFile);

        CV cv = parserService.parseResume(tempFile);
        Offer offer = parserService.parseJob(jobText);

        double score = matchingService.computeScore(cv, offer);

        Files.deleteIfExists(tempFile);

        Map<String, Object> response = new HashMap<>();
        response.put("score", score);
        response.put("percentage", Math.round(score * 100));
        response.put("message", "Matching effectué avec succès");

        return ResponseEntity.ok(response);

    } catch (Exception e) {
        return ResponseEntity.badRequest().body(
                Map.of(
                        "score", 0,
                        "percentage", 0,
                        "error", e.getMessage()
                )
        );
    }
}

}