package com.example.matching_back.record;

import java.util.List;

public record CV(
    String name,
    String email,
    String phoneNumber,
    String profession,
    List<Experience> experience,
    List<Education> education,
    List<String> skills,
    List<Language> languages, 
    List<String> certifications,
    double yearsOfExperience
) {}