import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="The Referee - Decision Making Tool",
    page_icon="⚖️",
    layout="wide"
)

# Options database
OPTIONS_DB = {
    'api': {
        'REST API': {
            'description': 'Simple, widely-adopted web service architecture',
            'pros': ['Simple and intuitive', 'Excellent caching', 'Wide tooling support', 'HTTP standard'],
            'cons': ['Over-fetching data', 'Multiple requests', 'Limited real-time', 'Versioning issues'],
            'performance': {'speed': 4, 'scalability': 4, 'reliability': 5},
            'complexity': {'setup': 2, 'maintenance': 2, 'learning': 1},
            'use_cases': ['CRUD operations', 'Public APIs', 'Mobile apps', 'Microservices']
        },
        'GraphQL': {
            'description': 'Query language for APIs with precise data fetching',
            'pros': ['Single endpoint', 'Precise data fetching', 'Strong typing', 'Real-time subscriptions'],
            'cons': ['Learning curve', 'Caching complexity', 'Query analysis needed', 'Expensive queries'],
            'performance': {'speed': 4, 'scalability': 3, 'reliability': 4},
            'complexity': {'setup': 4, 'maintenance': 3, 'learning': 4},
            'use_cases': ['Complex data', 'Mobile apps', 'Real-time apps', 'Developer tools']
        },
        'gRPC': {
            'description': 'High-performance RPC framework using HTTP/2',
            'pros': ['High performance', 'Strong typing', 'Streaming', 'Code generation'],
            'cons': ['Limited browser support', 'Binary complexity', 'Debugging hard', 'Learning curve'],
            'performance': {'speed': 5, 'scalability': 5, 'reliability': 5},
            'complexity': {'setup': 4, 'maintenance': 4, 'learning': 4},
            'use_cases': ['Microservices', 'High-performance', 'Streaming', 'Internal APIs']
        }
    },
    'cloud-service': {
        'AWS': {
            'description': 'Comprehensive cloud platform with 200+ services',
            'pros': ['Largest portfolio', 'Global infrastructure', 'Mature ecosystem', 'Enterprise features'],
            'cons': ['Complex pricing', 'Learning curve', 'Vendor lock-in', 'Can be expensive'],
            'performance': {'speed': 5, 'scalability': 5, 'reliability': 5},
            'complexity': {'setup': 4, 'maintenance': 4, 'learning': 5},
            'use_cases': ['Enterprise apps', 'Big data', 'ML/AI', 'Global scale']
        },
        'Azure': {
            'description': 'Microsoft cloud with strong enterprise integration',
            'pros': ['Microsoft integration', 'Hybrid cloud', 'Enterprise-friendly', 'AI/ML services'],
            'cons': ['Complex interface', 'Pricing complexity', 'Less mature', 'Learning curve'],
            'performance': {'speed': 4, 'scalability': 5, 'reliability': 4},
            'complexity': {'setup': 4, 'maintenance': 4, 'learning': 4},
            'use_cases': ['Microsoft environments', 'Hybrid cloud', 'Enterprise', 'AI projects']
        },
        'Google Cloud': {
            'description': 'Google cloud with strong data and AI capabilities',
            'pros': ['Data analytics', 'AI/ML services', 'Competitive pricing', 'Kubernetes support'],
            'cons': ['Smaller portfolio', 'Less enterprise features', 'Newer platform', 'Limited presence'],
            'performance': {'speed': 4, 'scalability': 4, 'reliability': 4},
            'complexity': {'setup': 3, 'maintenance': 3, 'learning': 3},
            'use_cases': ['Data analytics', 'Machine learning', 'Kubernetes', 'Startups']
        }
    },
    'database': {
        'PostgreSQL': {
            'description': 'Advanced open-source relational database',
            'pros': ['ACID compliant', 'Rich features', 'Extensible', 'Strong community'],
            'cons': ['Memory intensive', 'Complex config', 'Slower simple queries', 'Learning curve'],
            'performance': {'speed': 4, 'scalability': 4, 'reliability': 5},
            'complexity': {'setup': 3, 'maintenance': 3, 'learning': 3},
            'use_cases': ['Complex apps', 'Data warehousing', 'GIS apps', 'Financial systems']
        },
        'MongoDB': {
            'description': 'Document-oriented NoSQL database',
            'pros': ['Flexible schema', 'Horizontal scaling', 'Rich queries', 'Easy to start'],
            'cons': ['Memory usage', 'Consistency challenges', 'Complex aggregations', 'Enterprise costs'],
            'performance': {'speed': 4, 'scalability': 5, 'reliability': 4},
            'complexity': {'setup': 2, 'maintenance': 3, 'learning': 2},
            'use_cases': ['Content management', 'Real-time analytics', 'IoT apps', 'Prototyping']
        }
    }
}

def calculate_score(option_data: Dict, priorities: Dict) -> float:
    """Calculate weighted score based on priorities"""
    score = 0
    max_score = 0
    
    # Performance metrics
    if 'performance' in option_data:
        perf = option_data['performance']
        score += perf['speed'] * priorities['performance']
        score += perf['scalability'] * priorities['scalability'] 
        score += perf['reliability'] * priorities['reliability']
        max_score += 5 * (priorities['performance'] + priorities['scalability'] + priorities['reliability'])
    
    # Complexity (lower is better, so invert)
    if 'complexity' in option_data:
        comp = option_data['complexity']
        score += (6 - comp['setup']) * priorities['ease_of_use']
        score += (6 - comp['learning']) * priorities['ease_of_use']
        max_score += 5 * priorities['ease_of_use'] * 2
    
    # Cost (simplified)
    score += 3 * priorities['cost']
    max_score += 5 * priorities['cost']
    
    return (score / max_score * 5) if max_score > 0 else 3

def main():
    st.title("⚖️ The Referee")
    st.subheader("Smart Decision Making Tool - Compare Options & Understand Trade-offs")
    
    # Configuration in main area with columns
    st.markdown("## 🔧 Configuration")
    
    # Row 1: Category and Options
    col1, col2 = st.columns([1, 2])
    
    with col1:
        category = st.selectbox(
            "What are you comparing?",
            options=['api', 'cloud-service', 'database'],
            format_func=lambda x: {
                'api': '🔌 APIs & Services',
                'cloud-service': '☁️ Cloud Services', 
                'database': '🗄️ Databases'
            }[x]
        )
    
    with col2:
        available_options = list(OPTIONS_DB[category].keys())
        selected_options = st.multiselect(
            "Select 2-4 options to compare:",
            options=available_options,
            default=available_options[:2] if len(available_options) >= 2 else available_options
        )
    
    # Row 2: Requirements and Constraints
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Requirements**")
        requirements_text = st.text_area(
            "List your requirements:",
            placeholder="High availability\nReal-time data\nMobile support",
            key="requirements_input",
            height=100
        )
        requirements = requirements_text.split('\n') if requirements_text else []
    
    with col2:
        st.markdown("**🚫 Constraints**")
        constraints_text = st.text_area(
            "List your constraints:",
            placeholder="Budget under $1000/month\nTeam has limited experience\nMust integrate with existing system",
            key="constraints_input",
            height=100
        )
        constraints = constraints_text.split('\n') if constraints_text else []
    
    # Row 3: Priorities in a compact layout
    st.markdown("**🎯 Set Your Priorities (1=Low, 5=High)**")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        cost_priority = st.slider("� Cost", 1, 5, 3, key="cost")
    with col2:
        performance_priority = st.slider("⚡ Performance", 1, 5, 3, key="performance")
    with col3:
        ease_priority = st.slider("😊 Ease of Use", 1, 5, 3, key="ease")
    with col4:
        scalability_priority = st.slider("📈 Scalability", 1, 5, 3, key="scalability")
    with col5:
        reliability_priority = st.slider("🛡️ Reliability", 1, 5, 3, key="reliability")
    
    priorities = {
        'cost': cost_priority,
        'performance': performance_priority,
        'ease_of_use': ease_priority,
        'scalability': scalability_priority,
        'reliability': reliability_priority
    }
    
    st.markdown("---")
    
    # Validation and Compare button
    if len(selected_options) < 2:
        st.warning("⚠️ Please select at least 2 options to compare")
        return
    
    # Compare button - centered and prominent
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        compare_clicked = st.button("🔍 Compare Options", type="primary", use_container_width=True)
    
    if compare_clicked:
        st.markdown("---")
        
        # Calculate scores
        scored_options = []
        for option_name in selected_options:
            option_data = OPTIONS_DB[category][option_name]
            score = calculate_score(option_data, priorities)
            scored_options.append({
                'name': option_name,
                'data': option_data,
                'score': score
            })
        
        # Sort by score
        scored_options.sort(key=lambda x: x['score'], reverse=True)
        winner = scored_options[0]
        
        # Recommendation
        st.success(f"🏆 **Recommended: {winner['name']}** (Score: {winner['score']:.1f}/5)")
        
        confidence = min(5, max(1, round(winner['score'])))
        st.write(f"**Confidence:** {'⭐' * confidence} ({confidence}/5)")
        
        # Detailed comparison
        st.markdown("## 📊 Detailed Comparison")
        
        # Create comparison table
        comparison_data = []
        for option in scored_options:
            perf = option['data'].get('performance', {})
            comp = option['data'].get('complexity', {})
            
            comparison_data.append({
                'Option': option['name'],
                'Overall Score': f"{option['score']:.1f}/5",
                'Speed': f"{perf.get('speed', 'N/A')}/5",
                'Scalability': f"{perf.get('scalability', 'N/A')}/5", 
                'Reliability': f"{perf.get('reliability', 'N/A')}/5",
                'Setup Complexity': f"{comp.get('setup', 'N/A')}/5",
                'Learning Curve': f"{comp.get('learning', 'N/A')}/5"
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        # Detailed analysis for each option
        st.markdown("## 🔍 Detailed Analysis")
        
        cols = st.columns(len(selected_options))
        for i, option in enumerate(scored_options):
            with cols[i]:
                st.markdown(f"### {option['name']}")
                st.write(option['data']['description'])
                
                # Pros
                st.markdown("**✅ Pros:**")
                for pro in option['data']['pros']:
                    st.write(f"• {pro}")
                
                # Cons
                st.markdown("**❌ Cons:**")
                for con in option['data']['cons']:
                    st.write(f"• {con}")
                
                # Use cases
                st.markdown("**🎯 Best For:**")
                for use_case in option['data']['use_cases']:
                    st.write(f"• {use_case}")
        
        # Trade-offs analysis
        st.markdown("## ⚖️ Key Trade-offs")
        
        if len(scored_options) >= 2:
            opt1, opt2 = scored_options[0], scored_options[1]
            
            st.info(f"""
            **{opt1['name']} vs {opt2['name']}:**
            
            {opt1['name']} scores higher overall but consider:
            - {opt1['name']}: {', '.join(opt1['data']['pros'][:2])}
            - {opt2['name']}: {', '.join(opt2['data']['pros'][:2])}
            
            Choose {opt1['name']} if you prioritize {', '.join([k for k, v in priorities.items() if v >= 4][:2])}.
            Choose {opt2['name']} if you need {', '.join(opt2['data']['use_cases'][:2])}.
            """)
        
        # Summary
        st.markdown("## 📝 Summary")
        
        high_priorities = [k.replace('_', ' ') for k, v in priorities.items() if v >= 4]
        
        summary = f"""
        After analyzing {', '.join(selected_options)} based on your priorities, **{winner['name']}** 
        emerges as the recommended choice with a score of {winner['score']:.1f}/5.
        
        This recommendation particularly considers your high priority on {', '.join(high_priorities) if high_priorities else 'balanced factors'}.
        
        However, the final decision should consider your specific context, team expertise, and long-term goals. 
        Each option has its merits - the best choice depends on weighing these trade-offs against your unique situation.
        """
        
        st.write(summary)
        
        # Export options
        st.markdown("## 📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON export
            export_data = {
                'comparison': {
                    'category': category,
                    'options': selected_options,
                    'winner': winner['name'],
                    'scores': {opt['name']: opt['score'] for opt in scored_options},
                    'priorities': priorities,
                    'requirements': requirements,
                    'constraints': constraints
                }
            }
            
            st.download_button(
                "� Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name="comparison_results.json",
                mime="application/json"
            )
        
        with col2:
            # CSV export
            csv_data = pd.DataFrame(comparison_data).to_csv(index=False)
            st.download_button(
                "� Download CSV", 
                data=csv_data,
                file_name="comparison_results.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()