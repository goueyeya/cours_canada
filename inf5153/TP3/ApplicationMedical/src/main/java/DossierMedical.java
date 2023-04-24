import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.sql.Date;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DossierMedical {

    private int id;
    private String prenom;
    private String nom;
    private Date date;

}
