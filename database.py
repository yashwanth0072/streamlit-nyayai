"""
Database management for NyayAI - handles SQLite operations for IPC sections and templates
"""
import sqlite3
import json
from typing import List, Dict, Optional

class NyayAIDatabase:
    def __init__(self, db_path: str = "nyayai.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create IPC sections table with punishment information
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ipc_sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_number TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    applicable_context TEXT NOT NULL,
                    punishment TEXT NOT NULL,
                    category TEXT NOT NULL,
                    keywords TEXT NOT NULL
                )
            """)
            
            # Create legal templates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    template_content TEXT NOT NULL,
                    description TEXT NOT NULL
                )
            """)
            
            # Create query history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
            # Populate with sample data if empty
            self.populate_sample_data()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    def populate_sample_data(self):
        """Populate database with sample IPC sections and templates"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if data already exists
            cursor.execute("SELECT COUNT(*) FROM ipc_sections")
            if cursor.fetchone()[0] > 0:
                conn.close()
                return
        except sqlite3.Error as e:
            print(f"Error populating sample data: {e}")
            if 'conn' in locals():
                conn.close()
            return
        
        # Sample IPC sections with punishment details
        ipc_sections = [
            ("302", "Murder", "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.", 
             "Applies when someone intentionally causes death of another person with premeditation or during commission of another crime.", 
             "Death penalty or life imprisonment plus fine. Non-bailable and non-compoundable offense.", 
             "Offences against Human Body", "murder, killing, death, homicide"),
            
            ("376", "Rape", "Whoever commits rape shall be punished with rigorous imprisonment for a term not less than seven years.", 
             "Sexual assault against women without consent, including situations involving minors, public servants, or armed forces.", 
             "Minimum 7 years rigorous imprisonment, extendable to 10 years or life imprisonment plus fine. Death penalty in certain aggravated cases.", 
             "Offences against Women", "rape, sexual assault, women, crime"),
            
            ("420", "Cheating", "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property.", 
             "Fraudulent schemes, fake investments, document forgery, online scams, or any deception to obtain money/property.", 
             "Imprisonment up to 7 years and fine. Cognizable, non-bailable offense. Victim can file complaint.", 
             "Offences against Property", "cheating, fraud, dishonesty, property"),
            
            ("498A", "Cruelty by husband or relatives", "Whoever subjects any woman to cruelty shall be punished with imprisonment.", 
             "Domestic violence, dowry harassment, mental/physical torture by husband or in-laws after marriage.", 
             "Imprisonment up to 3 years and fine. Non-bailable, cognizable offense. Special courts handle such cases.", 
             "Offences against Women", "dowry, harassment, cruelty, domestic violence"),
            
            ("354", "Assault on women", "Whoever assaults or uses criminal force to any woman, intending to outrage her modesty.", 
             "Inappropriate touching, sexual harassment, stalking, or any act intended to outrage woman's modesty.", 
             "Imprisonment from 1 to 5 years and fine. Cognizable, non-bailable offense with fast-track courts.", 
             "Offences against Women", "assault, women, modesty, harassment"),
            
            ("379", "Theft", "Whoever intends to take dishonestly any movable property out of the possession of any person.", 
             "Stealing money, goods, vehicles, or any movable property without owner's consent from any place.", 
             "Imprisonment up to 3 years or fine or both. Bailable offense. Punishment increases for repeat offenders.", 
             "Offences against Property", "theft, stealing, property, dishonesty"),
            
            ("323", "Voluntarily causing hurt", "Whoever voluntarily causes hurt shall be punished with imprisonment.", 
             "Physical assault causing pain, injury, or harm but not endangering life or causing grievous hurt.", 
             "Imprisonment up to 1 year or fine up to ₹1000 or both. Bailable, non-cognizable offense.", 
             "Offences against Human Body", "hurt, injury, assault, violence"),
            
            ("506", "Criminal intimidation", "Whoever commits criminal intimidation shall be punished with imprisonment.", 
             "Threatening someone with injury to person, reputation, or property to cause alarm or coerce action.", 
             "Imprisonment up to 2 years or fine or both. If threat is of death/grievous hurt, up to 7 years imprisonment.", 
             "Offences against Public Tranquility", "intimidation, threat, fear, criminal"),
            
            ("294", "Obscene acts", "Whoever does any obscene act in any public place shall be punished.", 
             "Singing, reciting, or uttering obscene songs, ballads, or words in public places causing annoyance.", 
             "Imprisonment up to 3 months or fine or both. Bailable offense handled by magistrate courts.", 
             "Offences against Public Tranquility", "obscenity, public nuisance, indecency"),
            
            ("406", "Criminal breach of trust", "Whoever commits criminal breach of trust shall be punished.", 
             "Misappropriation of money/property entrusted by employer, client, or in fiduciary capacity.", 
             "Imprisonment up to 3 years or fine or both. Non-bailable if amount exceeds certain limits.", 
             "Offences against Property", "breach of trust, embezzlement, misappropriation")
        ]
        
        cursor.executemany("""
            INSERT INTO ipc_sections (section_number, title, description, applicable_context, punishment, category, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ipc_sections)
        
        # Sample legal templates
        templates = [
            ("Rental Agreement", "Property", 
             """RENTAL AGREEMENT

This agreement is made between:
Landlord: [LANDLORD_NAME]
Tenant: [TENANT_NAME]

Property Address: [PROPERTY_ADDRESS]
Monthly Rent: Rs. [RENT_AMOUNT]
Security Deposit: Rs. [DEPOSIT_AMOUNT]
Lease Period: [LEASE_PERIOD]

Terms and Conditions:
1. Rent to be paid by [PAYMENT_DATE] of each month
2. Security deposit refundable upon vacating
3. No subletting without written consent
4. Maintenance of property is tenant's responsibility

Signatures:
Landlord: ________________
Tenant: ________________
Date: ________________""", 
             "Standard rental agreement template for residential properties"),
            
            ("Employment Contract", "Employment",
             """EMPLOYMENT AGREEMENT

Employee: [EMPLOYEE_NAME]
Employer: [COMPANY_NAME]
Position: [JOB_TITLE]
Start Date: [START_DATE]
Salary: Rs. [SALARY_AMOUNT] per month

Job Responsibilities:
[JOB_DESCRIPTION]

Terms:
1. Probation period: [PROBATION_PERIOD]
2. Working hours: [WORKING_HOURS]
3. Leave entitlement: [LEAVE_DAYS] days per year
4. Notice period: [NOTICE_PERIOD]

Employee Signature: ________________
Employer Signature: ________________
Date: ________________""",
             "Basic employment contract template"),
            
            ("Legal Notice", "Legal Proceedings",
             """LEGAL NOTICE

To: [RECIPIENT_NAME]
Address: [RECIPIENT_ADDRESS]

Subject: [NOTICE_SUBJECT]

Dear Sir/Madam,

I, [SENDER_NAME], through this legal notice, bring to your attention the following:

[NOTICE_CONTENT]

You are hereby called upon to [DEMANDED_ACTION] within [TIME_PERIOD] days from receipt of this notice, failing which my client will be constrained to initiate appropriate legal proceedings against you.

This notice is issued without prejudice to any other rights and remedies available to my client.

Yours faithfully,
[ADVOCATE_NAME]
Advocate for [CLIENT_NAME]""",
             "Legal notice template for various disputes")
        ]
        
        cursor.executemany("""
            INSERT INTO legal_templates (template_name, category, template_content, description)
            VALUES (?, ?, ?, ?)
        """, templates)
        
        conn.commit()
        conn.close()
    
    def search_ipc_sections(self, query: str) -> List[Dict]:
        """Search IPC sections by keywords or section number"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT section_number, title, description, applicable_context, punishment, category
                FROM ipc_sections
                WHERE keywords LIKE ? OR section_number LIKE ? OR title LIKE ?
                ORDER BY section_number
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        except sqlite3.Error as e:
            print(f"Error searching IPC sections: {e}")
            return []
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "section": row[0],
                "title": row[1],
                "description": row[2],
                "context": row[3],
                "punishment": row[4],
                "category": row[5]
            })
        
        conn.close()
        return results
    
    def get_all_ipc_sections(self) -> List[Dict]:
        """Get all IPC sections"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT section_number, title, description, applicable_context, punishment, category
                FROM ipc_sections
                ORDER BY CAST(section_number AS INTEGER)
            """)
        except sqlite3.Error as e:
            print(f"Error getting IPC sections: {e}")
            return []
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "section": row[0],
                "title": row[1],
                "description": row[2],
                "context": row[3],
                "punishment": row[4],
                "category": row[5]
            })
        
        conn.close()
        return results
    
    def get_legal_templates(self, category: str = None) -> List[Dict]:
        """Get legal templates, optionally filtered by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT template_name, category, template_content, description
                    FROM legal_templates
                    WHERE category = ?
                """, (category,))
            else:
                cursor.execute("""
                    SELECT template_name, category, template_content, description
                    FROM legal_templates
                """)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "name": row[0],
                    "category": row[1],
                    "content": row[2],
                    "description": row[3]
                })
            
            conn.close()
            return results
        except sqlite3.Error as e:
            print(f"Error getting legal templates: {e}")
            return []
    
    def save_query(self, query: str, response: str):
        """Save query and response to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO query_history (query, response)
                VALUES (?, ?)
            """, (query, response))
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error saving query history: {e}")