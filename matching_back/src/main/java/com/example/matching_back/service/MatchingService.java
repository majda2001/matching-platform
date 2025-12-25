package com.example.matching_back.service;

import com.example.matching_back.record.CV;
import com.example.matching_back.record.Offer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import java.util.Map;

@Service
public class MatchingService {

    private final WebClient webClient;

    @Value("${spring.ai.ollama.base-url}")
    private String ollamaBaseUrl; 

    public MatchingService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

    public double computeScore(CV cv, Offer offer) {
        try {
           
            String prompt = String.format(
                """
    Agis en tant qu'expert en recrutement. Tu dois évaluer le matching entre un CV et une Offre selon ce barème précis :
    1. Niveau et domaine d'études : Est-ce que le diplôme correspond au domaine demandé ?
    2. Compétences techniques : Analyse la maîtrise des outils requis.
    3. Expérience : Compare les années et la pertinence des postes.
    4. Certifications : Si l'offre en demande une, vérifie sa présence. Si le CV en a sans qu'elles soient demandées, donne un bonus de score si elles sont pertinentes.

    CV à analyser : %s
    Offre d'emploi : %s

    Retourne UNIQUEMENT un score final entre 0 et 1 (ex: 0.85). Ne donne aucune explication.
    """, 
    cv.toString(), offer.toString()
);
         
            Map<String, Object> requestBody = Map.of(
                "model", "llama3",
                "prompt", prompt,
                "stream", false
            );

           
            Map<String, Object> result = webClient.post()
                    .uri(ollamaBaseUrl + "/api/generate")
                    .bodyValue(requestBody)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

           
            if (result != null && result.containsKey("response")) {
                String rawResponse = result.get("response").toString().trim();
               
                String cleanResponse = rawResponse.replaceAll("[^0-9.]", "");
                return Double.parseDouble(cleanResponse);
            }

            return 0.0;

        } catch (Exception e) {
            System.err.println("Erreur Ollama : " + e.getMessage());
            return 0.0;
        }
    }
}