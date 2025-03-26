import pandas as pd
import re
from difflib import SequenceMatcher
from openpyxl import load_workbook
from io import BytesIO

class DataPreprocessor:
    def __init__(self):
        self.author_name_mapping = {}  # İsimlerin standartlaştırılmış hallerini tutacak
        self.name_standardization_log = []  # İsim değişikliklerini loglamak için
        
    def clean_author_name(self, name: str) -> str:
        """
        Yazar ismini standart bir formata dönüştürür.
        """
        if not isinstance(name, str):
            return ""
            
        # Boşlukları temizle ve noktalama işaretlerini kaldır
        name = name.strip()
        name = re.sub(r'[.,;:]', '', name)  # Noktalama işaretlerini kaldır
        name = re.sub(r'\s+', ' ', name)  # Birden fazla boşluğu teke indir
        
        return name
    def get_name_parts(self, name: str) -> tuple:
        """
        İsmi soyadı ve ilk isim/inisyal olarak ayırır
        """
        parts = name.split()
        if len(parts) == 1:
            return parts[0], ""
        
        surname = parts[-1]
        first_parts = " ".join(parts[:-1])
        return surname, first_parts

    
    def names_are_similar(self, name1: str, name2: str) -> tuple:
        """
        İki ismin benzer olup olmadığını kontrol eder.
        Daha katı kurallar uygular.
        """
        # İsimleri parçala
        surname1, first1 = self.get_name_parts(name1)
        surname2, first2 = self.get_name_parts(name2)
        
        # Soyadları tam eşleşmeli
        if surname1 != surname2:
            return False, 0, None
            
        # Soyadı eşleşiyorsa, isim kısımlarını kontrol et
        similarity = SequenceMatcher(None, first1, first2).ratio()
        
        # Benzerlik kontrolü için katı kurallar
        if similarity > 0.90:
            # İsimleri kelimelerine ayır
            words1 = set(first1.split())
            words2 = set(first2.split())
            
            # Eğer bir tarafta inisyal varsa (tek harfli kelime)
            has_initial1 = any(len(word) == 1 for word in words1)
            has_initial2 = any(len(word) == 1 for word in words2)
            
            # İnisyal ve tam isim kontrolü
            if has_initial1 and not has_initial2:
                # İnisyaller tam isimle eşleşmeli
                for init in words1:
                    if len(init) == 1:
                        matching_full = False
                        for full in words2:
                            if full.startswith(init):
                                matching_full = True
                                break
                        if not matching_full:
                            return False, similarity, None
                return True, similarity, name2  # Tam ismi tercih et
                
            elif has_initial2 and not has_initial1:
                # İnisyaller tam isimle eşleşmeli
                for init in words2:
                    if len(init) == 1:
                        matching_full = False
                        for full in words1:
                            if full.startswith(init):
                                matching_full = True
                                break
                        if not matching_full:
                            return False, similarity, None
                return True, similarity, name1  # Tam ismi tercih et
                
            # Her iki isimde de inisyal varsa veya ikisi de tam isimse
            elif len(first1) > len(first2):
                return True, similarity, name1
            else:
                return True, similarity, name2
                
        return False, similarity, None

    def update_author_references(self, df: pd.DataFrame, old_name: str, new_name: str):
        """
        Bir yazarın ismini günceller ve tüm referansları günceller
        """
        # Coauthors listelerindeki eski isimleri güncelle
        df['coauthors'] = df['coauthors'].apply(
            lambda authors: [new_name if author == old_name else author for author in authors]
        )
        
        # Ana yazar ismini güncelle
        df['author_name'] = df['author_name'].replace(old_name, new_name)
        
        return df

    def standardize_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Yazar isimlerini standartlaştırır ve loglar.
        """
        standardized_names = []
        for name in df['author_name']:
            standardized_name = self.clean_author_name(name)
            standardized_names.append(standardized_name)
            if name != standardized_name:
                self.name_standardization_log.append((name, standardized_name))
        
        df['author_name'] = standardized_names
        
        # İsim değişikliklerini logla
        with open('name_standardization_log.txt', 'w', encoding='utf-8') as f:
            for original, standardized in self.name_standardization_log:
                f.write(f"{original} -> {standardized}\n")
        
        return df

    def parse_coauthors(self, coauthors_str: str) -> list:
        """
        Coauthors sütunundaki string'i parse eder ve temizler
        """
        try:
            if isinstance(coauthors_str, str):
                # String'i liste haline getir
                authors = coauthors_str.strip('[]').split(',')
                # Her bir yazarı temizle
                authors = [self.clean_author_name(author.strip().strip("'\"")) for author in authors]
                # Boş stringleri kaldır
                authors = [author for author in authors if author]
                return authors
            return []
        except Exception as e:
            print(f"Coauthors parsing error: {e}")
            return []

    

    def load_and_clean_data(self, file_path: str) -> pd.DataFrame:
        """
        Excel dosyasını okur ve temizler.
        
        Args:
            file_path (str): Excel dosyasının yolu
            
        Returns:
            pd.DataFrame: Temizlenmiş veri çerçevesi
        
        Raises:
            FileNotFoundError: Dosya bulunamazsa
            ValueError: Dosya formatı geçersizse
        """
        try:
            # Excel dosyasını pandas ile oku
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Boş DataFrame kontrolü
            if df.empty:
                raise ValueError("Excel dosyası boş")
                
            # Gerekli sütunların varlığını kontrol et
            required_columns = {'author_name', 'coauthors', 'paper_title', 'doi'}
            if not required_columns.issubset(set(map(str.lower, df.columns))):
                missing = required_columns - set(map(str.lower, df.columns))
                raise ValueError(f"Eksik sütunlar: {missing}")
            
            # Sütun isimlerini standardize et
            df.columns = [str(col).lower().replace(' ', '_') for col in df.columns]
            
            # String dönüşümlerini güvenli hale getir
            def safe_str(x):
                if pd.isna(x):
                    return ""
                try:
                    return str(x).encode('utf-8', errors='ignore').decode('utf-8')
                except:
                    return str(x)
            
            # NaN değerleri temizle
            df = df.dropna(subset=['author_name', 'coauthors', 'paper_title'])
            
            # Tüm string kolonları güvenli hale getir
            df['author_name'] = df['author_name'].apply(safe_str)
            df['paper_title'] = df['paper_title'].apply(safe_str)
            df['doi'] = df['doi'].apply(safe_str)
            df['coauthors'] = df['coauthors'].apply(safe_str)
            
            # Coauthors sütununu parse et
            df['coauthors'] = df['coauthors'].apply(self.parse_coauthors)
            
            # Ana yazar isimlerini temizle
            df['author_name'] = df['author_name'].apply(self.clean_author_name)
            
            # Coauthors isimlerini temizle
            df['coauthors'] = df['coauthors'].apply(
                lambda authors: [self.clean_author_name(author) for author in authors]
            )
            
            # İsimleri standartlaştır
            df = self.standardize_names(df)
            
            # Duplicate kayıtları kontrol et
            df = df.drop_duplicates(subset=['doi', 'author_name'])
            
            print(f"Veri başarıyla yüklendi: {len(df)} kayıt")
            return df
            
        except FileNotFoundError:
            print(f"Hata: '{file_path}' dosyası bulunamadı")
            return pd.DataFrame()
        except pd.errors.EmptyDataError:
            print("Hata: Excel dosyası boş veya okunamıyor")
            return pd.DataFrame()
        except Exception as e:
            print(f"Veri yükleme hatası: {str(e)}")
            import traceback
            print(traceback.format_exc())  # Detaylı hata mesajı
            return pd.DataFrame()

    def print_standardization_report(self):
        """
        İsim standardizasyonu raporunu yazdırır
        """
        print("\nİsim Standardizasyonu Raporu:")
        print("-" * 50)
        for log in sorted(self.name_standardization_log, 
                         key=lambda x: x['similarity'], reverse=True):
            print(f"Orijinal isimler: {' ve '.join(log['original_names'])}")
            print(f"Standardize edilmiş isim: {log['standardized_name']}")
            print(f"Benzerlik oranı: {log['similarity']:.2f}")
            print("-" * 50)

