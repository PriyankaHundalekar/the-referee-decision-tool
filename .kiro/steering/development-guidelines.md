# Development Guidelines for The Referee

## Project Overview
The Referee is a decision-making tool that compares options and explains trade-offs instead of giving single answers. Built for the AI for Bharat hackathon Week 6 challenge.

## Architecture Principles

### Streamlit Application (Python)
- Single-file application with clean separation of concerns
- Python for data processing and comparison logic
- Streamlit for interactive web interface
- Modular functions for business logic
- Built-in responsive design

## Code Standards

### Python
- Use type hints where appropriate
- Follow PEP 8 style guidelines
- Use descriptive function and variable names
- Proper error handling with try-except blocks
- Modular functions for reusability

### Streamlit Components
- Clear separation between UI and logic
- Use st.cache for expensive operations
- Responsive layout with columns and containers
- Consistent styling with Streamlit themes

## Comparison Logic Guidelines

### Adding New Categories
1. Define options in OPTIONS_DB dictionary
2. Include all required fields: pros, cons, performance, complexity, use_cases
3. Add realistic scoring metrics (1-5 scale)
4. Test with various priority combinations

### Scoring Algorithm
- Performance metrics: speed, scalability, reliability (1-5 scale)
- Complexity metrics: setup, maintenance, learning (1-5 scale, lower is better)
- Weighted scoring based on user priorities
- Confidence calculation based on score differences

## Deployment Considerations

### Streamlit Cloud Ready
- Single Python file deployment
- Requirements.txt for dependencies
- Environment variables for configuration
- Built-in sharing and collaboration features

### Performance Optimization
- Use st.cache for data loading
- Optimize pandas operations
- Minimize recomputation with session state
- Efficient data structures

## Testing Strategy
- Unit tests for comparison logic functions
- Streamlit app testing with pytest
- Data validation tests
- User workflow testing

## Future Enhancements
- Real-time collaboration with Streamlit sharing
- Integration with external APIs for live data
- Machine learning for improved recommendations
- Advanced visualization with Plotly
- User preferences and saved comparisons