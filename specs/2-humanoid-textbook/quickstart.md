# Quickstart Guide: Humanoid Robotics Textbook Development

## Prerequisites
- Python 3.11+
- Node.js 18+
- Git
- Docker (optional, for local development)

## Setup Development Environment

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the backend server:
   ```bash
   python -m src.main
   ```

### Frontend Setup
1. Navigate to the website directory:
   ```bash
   cd website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm start
   ```

## Key Configuration

### Environment Variables
- `DATABASE_URL`: Connection string for Neon Postgres database
- `AUTH_SECRET`: Secret key for Better-Auth
- `LLM_API_KEY`: API key for translation services
- `NEXT_PUBLIC_BASE_URL`: Base URL for the application

### Database Setup
1. Install the Neon CLI or use the web interface
2. Create a new project and database
3. Update `DATABASE_URL` in your environment variables
4. Run migrations (if applicable)

## Running Tests
- Backend tests: `pytest tests/`
- Frontend tests: `npm test`
- Integration tests: `pytest tests/integration/`

## Building for Production
- Backend: `python -m build` (if applicable)
- Frontend: `npm run build`

## Deployment
The application is designed for deployment to GitHub Pages:
1. Build the frontend: `npm run build`
2. The output will be in the `build/` directory
3. Configure GitHub Pages to serve from the `build/` directory

## Common Tasks

### Adding a New Chapter
1. Create a new Markdown file in `website/docs/`
2. Add proper frontmatter with metadata
3. Update `website/sidebars.js` to include the new chapter

### Adding Personalization Logic
1. Create personalization rules in the backend service
2. Update the personalization API endpoint
3. Add frontend components to handle personalized content display

### Adding Translation Support
1. Update the translation service with new language support
2. Ensure proper handling of technical terminology
3. Test translation quality and performance

## Troubleshooting

### Common Issues
- **Database connection errors**: Check your `DATABASE_URL` environment variable
- **Authentication not working**: Verify `AUTH_SECRET` is set correctly
- **Translation API errors**: Confirm your `LLM_API_KEY` is valid and has sufficient quota

### Development Tips
- Use the `--watch` flag when developing to automatically reload changes
- Check the logs for detailed error information
- Use the staging environment for testing before production deployment