package com.example.matching_back.record;

import java.util.List;

public record Offer(
    String jobTitle,
    String companyName,
    List<String> competences,
    String requiredExperienceYears,
    List<Language> requiredLanguages,
    List<String> certifications,
    List<Education> educations
) {}