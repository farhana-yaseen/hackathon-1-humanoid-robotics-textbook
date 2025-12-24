# Task List: Authentication Redirect & Urdu Translation

**Feature**: Authentication Redirect & Urdu Translation
**Branch**: 3-auth-redirect-urdu-translation
**Generated**: 2025-12-21
**Spec**: [specs/3-auth-redirect-urdu-translation/spec.md](../spec.md)
**Plan**: [specs/3-auth-redirect-urdu-translation/plan/impl-plan.md](plan/impl-plan.md)

## Overview

This task list implements the authentication redirect to Module Page and Urdu translation functionality. The implementation follows the user stories from the specification with proper prioritization and dependencies.

## Dependencies

User stories can be implemented in parallel after foundational tasks are complete. User Story 1 (redirect) should be completed before User Story 2 (translation) for optimal user experience, but they can be developed independently.

## Parallel Execution Examples

- Database schema changes can run in parallel with frontend component updates
- Backend API endpoints can be developed while frontend UI is being created
- Translation caching can be implemented separately from the translation UI

## Implementation Strategy

- **MVP Scope**: User Story 1 (redirect) with basic translation functionality
- **Incremental Delivery**: Add advanced translation features and caching in later phases
- **Non-Breaking**: All changes are additive and preserve existing functionality

---

## Phase 1: Setup

Setup tasks to prepare the environment for implementation.

- [X] T001 Create database migration files for new tables
- [X] T002 Update environment variables documentation with new required variables
- [X] T003 Set up database connection for session extension tables
- [X] T004 Install required dependencies for caching and translation features

## Phase 2: Foundational

Foundational tasks that block all user stories.

- [X] T005 Create UserSessionExtension model in backend
- [X] T006 Create TranslationCache model in backend
- [X] T007 Create ModuleAccessLog model in backend
- [X] T008 Implement database repository classes for new models
- [X] T009 Update Better-Auth configuration to handle post-authentication redirects
- [X] T010 Create utility functions for content hashing and cache key generation

## Phase 3: User Story 1 - Direct Module Access After Login (Priority: P1)

As a user, after successful sign-in, I want to be redirected directly to the Module Page instead of the Home Page, so I can immediately access my learning content without extra navigation steps.

**Independent Test**: User logs in successfully and lands directly on the Module Page, skipping the Home Page entirely.

### Tests
- [ ] T011 [US1] Write unit tests for redirect logic with last accessed module
- [ ] T012 [US1] Write unit tests for default module fallback logic
- [ ] T013 [US1] Write integration tests for post-authentication redirect flow

### Implementation
- [ ] T014 [P] [US1] Update Better-Auth callback to redirect to Module Page instead of Home Page
- [ ] T015 [P] [US1] Implement database query to retrieve last accessed module for user
- [ ] T016 [US1] Create default module identifier for new users
- [ ] T017 [US1] Implement module access tracking when user visits a module page
- [ ] T018 [US1] Update frontend routing to handle module-specific URLs
- [ ] T019 [US1] Create API endpoint to record module access with position tracking
- [ ] T020 [US1] Update authentication success redirect logic in auth callback

## Phase 4: User Story 2 - Urdu Translation Capability (Priority: P1)

As a user on the Module Page, I want a "Translate to Urdu" button that translates the current chapter content to Urdu, so I can access educational content in my preferred language.

**Independent Test**: User clicks the "Translate to Urdu" button and sees the chapter content translated to Urdu without page reload.

### Tests
- [ ] T021 [US2] Write unit tests for translation API endpoint
- [ ] T022 [US2] Write unit tests for content formatting preservation
- [ ] T023 [US2] Write integration tests for translation button functionality

### Implementation
- [ ] T024 [P] [US2] Create backend API endpoint for content translation
- [ ] T025 [P] [US2] Integrate with Gemini API for Urdu translation
- [ ] T026 [US2] Implement loading indicator during translation process
- [ ] T027 [US2] Add "Translate to Urdu" button to module pages
- [ ] T028 [US2] Create frontend component for translation state management
- [ ] T029 [US2] Implement content replacement without page reload
- [ ] T030 [US2] Preserve formatting (headings, paragraphs, lists) in translated content

## Phase 5: User Story 3 - Translation Toggle & Formatting (Priority: P2)

As a user, I want to be able to toggle between English and Urdu content and see proper formatting preserved during translation, so I can switch languages as needed and maintain readability.

**Independent Test**: User can switch between English and Urdu versions of the same content while preserving formatting like headings and paragraphs.

### Tests
- [ ] T031 [US3] Write unit tests for language toggle functionality
- [ ] T032 [US3] Write unit tests for formatting preservation during toggling
- [ ] T033 [US3] Write integration tests for language preference persistence

### Implementation
- [ ] T034 [P] [US3] Implement language preference persistence in browser storage
- [ ] T035 [P] [US3] Add toggle functionality to switch between English and Urdu
- [ ] T036 [US3] Create "Translate to English" button when content is in Urdu
- [ ] T037 [US3] Implement session storage for language preference within module
- [ ] T038 [US3] Ensure formatting is preserved when toggling between languages

## Phase 6: Advanced Features

Advanced functionality to enhance the user experience based on clarifications.

### Caching Implementation
- [ ] T039 [P] Implement translation caching with 24-hour expiration
- [ ] T040 [P] Create cache invalidation mechanism for expired entries
- [ ] T041 Add cache lookup before making Gemini API calls

### Error Handling
- [ ] T042 Implement translation timeout with 30-second limit and progress indicator
- [ ] T043 Create error handling for Gemini API failures
- [ ] T044 Show error message while keeping original content visible on failure
- [ ] T045 Implement fallback to original content when translation fails

## Phase 7: Polish & Cross-Cutting Concerns

Final integration and quality improvements.

### Integration Testing
- [ ] T046 End-to-end test of authentication redirect flow
- [ ] T047 End-to-end test of translation functionality
- [ ] T048 Test error scenarios for translation API
- [ ] T049 Performance test for translation response times

### Documentation & Polish
- [ ] T050 Update API documentation with new endpoints
- [ ] T051 Add user documentation for new features
- [ ] T052 Update README with new functionality
- [ ] T053 Perform final code review and cleanup
- [ ] T054 Run all tests to ensure no regression in existing functionality