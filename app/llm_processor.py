import re

class ContractAnalyzer:
    def __init__(self):
        pass
    
    def extract_dates(self, text):
        # More comprehensive date patterns
        date_patterns = [
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',  # 12 Jan 2025
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # January 12, 2025
            r'\b\d{1,2}\s+\w+\s+\d{4}\b',  # 12 January 2025
            r'\b\d{4}\b'  # Standalone years
        ]
        
        dates = []
        for pattern in date_patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            # Handle different return types from regex
            for match in found:
                if isinstance(match, tuple):
                    # Join tuple elements
                    date_str = ' '.join([item for item in match if item])
                    if date_str and len(date_str) > 2:
                        dates.append(date_str)
                else:
                    if len(match) > 2:
                        dates.append(match)
        
        return list(set(dates))[:10]  # Remove duplicates, return top 10
    
    def extract_obligations(self, text):
        # More comprehensive obligation patterns
        obligation_keywords = [
            'shall', 'must', 'will', 'agree to', 'responsible for', 
            'obligated to', 'required to', 'ensure', 'guarantee',
            'warrant', 'covenant', 'undertake'
        ]
        
        # Split by lines and sentences
        lines = text.split('\n')
        obligations = []
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in obligation_keywords):
                clean_line = line.strip()
                if len(clean_line) > 10 and len(clean_line) < 500:  # Reasonable length
                    obligations.append(clean_line)
        
        # Also check bullet points specifically
        bullet_points = re.findall(r'[•\-*]\s*([^\.!?]*(?:shall|must|will|agree to|responsible for)[^\.!?]*[\.!?])', text, re.IGNORECASE)
        obligations.extend(bullet_points)
        
        return list(set(obligations))[:8]  # Remove duplicates, return top 8
    
    def extract_risks(self, text):
        risk_keywords = {
            '🔴 High Risk': ['penalty', 'termination', 'liable', 'indemnify', 'breach', 'damages', 'lawsuit', 'fraud', 'negligence'],
            '🟡 Medium Risk': ['warranty', 'guarantee', 'compliance', 'audit', 'inspection', 'default', 'confidential'],
            '🟢 Low Risk': ['notice', 'amendment', 'renewal', 'governing law']
        }
        
        risks = []
        text_lower = text.lower()
        
        for level, keywords in risk_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Find context around the keyword
                    context_pattern = f"[^.]*{keyword}[^.]*\."
                    contexts = re.findall(context_pattern, text_lower, re.IGNORECASE)
                    
                    if contexts:
                        context = contexts[0].strip()[:150] + "..."
                    else:
                        context = f"Found '{keyword}' in contract"
                    
                    risks.append({
                        'risk': keyword,
                        'level': level,
                        'description': context
                    })
                    break  # Only report each keyword once
        
        return risks[:8]
    
    def extract_financial_terms(self, text):
        # Extract payment amounts and financial terms
        financial_patterns = [
            r'₹\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # Indian Rupees
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*INR',  # INR amounts
            r'(\d+%|\d+\s*percent)',  # Percentages
        ]
        
        financials = []
        for pattern in financial_patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            financials.extend(found)
        
        return financials[:5]
    
    def generate_summary(self, text):
        summary_parts = []
        
        # Check for key contract sections
        if any(word in text.lower() for word in ['payment', 'fee', 'price', 'retainer']):
            financials = self.extract_financial_terms(text)
            if financials:
                summary_parts.append(f"• Financial terms: {', '.join(financials)}")
            else:
                summary_parts.append("• Payment terms specified")
        
        if any(word in text.lower() for word in ['confidential', 'proprietary', 'non-disclosure']):
            summary_parts.append("• Confidentiality obligations included")
        
        if any(word in text.lower() for word in ['termination', 'terminate', 'cancel']):
            summary_parts.append("• Termination clauses defined")
        
        if any(word in text.lower() for word in ['liable', 'liability', 'responsible', 'damages']):
            summary_parts.append("• Liability and risk allocation")
        
        if any(word in text.lower() for word in ['service', 'deliverable', 'obligation', 'duty']):
            summary_parts.append("• Service scope and deliverables outlined")
        
        dates = self.extract_dates(text)
        if dates:
            summary_parts.append(f"• Key dates: {', '.join(dates[:3])}")
        
        if summary_parts:
            return "Contract Summary:\n" + "\n".join(summary_parts)
        else:
            return "Standard legal agreement with general terms and conditions."
    
    def analyze_contract(self, text):
        try:
            dates = self.extract_dates(text)
            obligations = self.extract_obligations(text)
            risks = self.extract_risks(text)
            financials = self.extract_financial_terms(text)
            summary = self.generate_summary(text)
            
            return {
                "dates_deadlines": dates,
                "obligations": obligations,
                "risks": risks,
                "financials": financials,
                "summary": summary,
                "status": "✅ Analysis Complete"
            }
            
        except Exception as e:
            return {
                "dates_deadlines": [],
                "obligations": [],
                "risks": [],
                "financials": [],
                "summary": f"Analysis failed: {str(e)}",
                "status": "❌ Error"
            }

# Global analyzer instance
analyzer = ContractAnalyzer()