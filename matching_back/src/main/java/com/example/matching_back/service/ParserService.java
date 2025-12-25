package com.example.matching_back.service;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import org.springframework.core.io.FileSystemResource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.example.matching_back.record.CV;
import com.example.matching_back.record.Offer;

@Service
public class ParserService {

    private final WebClient webClient;
    private static final Logger log = LoggerFactory.getLogger(ParserService.class);

    public ParserService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

   public CV parseResume(Path resumePath) {
    try {
        if (!Files.exists(resumePath)) {
            throw new IllegalArgumentException("File not found: " + resumePath);
        }

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", new FileSystemResource(resumePath.toFile()));

        return webClient.post()
                .uri("http://localhost:8001/parse-cv")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .bodyValue(body)
                .retrieve()
                .bodyToMono(CV.class)
                .block();
    } catch (WebClientResponseException e) {
        log.error("CV parser returned {}: {}", e.getStatusCode(), e.getResponseBodyAsString(), e);
        throw new IllegalStateException("CV parser error: " + e.getStatusCode() + " " + e.getResponseBodyAsString(), e);
    } catch (Exception e) {
        log.error("Error calling CV parser", e);
        throw new IllegalStateException("Error calling CV parser", e);
    }
}

    public Offer parseJob(String jobText) {
    Map<String, String> body = Map.of("text", jobText);
    try {
        return webClient.post()
                .uri("http://localhost:8002/parse-job")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Offer.class)
                .block();
    } catch (WebClientResponseException e) {
        log.error("Job parser returned {}: {}", e.getStatusCode(), e.getResponseBodyAsString(), e);
        throw new IllegalStateException("Job parser error: " + e.getStatusCode() + " " + e.getResponseBodyAsString(), e);
    } catch (Exception e) {
        log.error("Error calling Job parser", e);
        throw new IllegalStateException("Error calling Job parser", e);
    }
}

}
